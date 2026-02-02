import os
import shutil
import pandas as pd
from app.processor import DataProcessor

class ValidationError(Exception):
    pass


class DataValidator:
    def __init__(self, config, logger):
        self.input_format = config["input_format"].lower()
        self.input_path = config["input_path"]
        self.output_path = config["output_path"]
        self.failed_path = config["failed_path"]
        self.required_columns = set(config["required_columns"])
        self.logger = logger

        os.makedirs(self.output_path, exist_ok=True)
        os.makedirs(self.failed_path, exist_ok=True)

    def validate_all(self):
        files = os.listdir(self.input_path)
        if not files:
            self.logger.info("No input files found")
            return

        for file in files:
            try:
                self._validate_file(file)
                self.logger.info(f"Validated successfully: {file}")
            except Exception as e:
                self.logger.error(f"Validation failed for {file}: {e}")
                self._move_to_failed(file)

    def _validate_file(self, filename):
        file_path = os.path.join(self.input_path, filename)

        if self.input_format == "csv":
         df = pd.read_csv(file_path)
        elif self.input_format == "json":
            df = pd.read_json(file_path)
        else:
            raise ValidationError(f"Unsupported format: {self.input_format}")

        self._validate_schema(df)
        self._validate_data(df)

        processor = DataProcessor(self.logger)
        processed_df = processor.process(df)

        output_file = os.path.join(self.output_path, filename)
        self.logger.info(f"Writing output to: {output_file}")
        processed_df.to_csv(output_file, index=False)

    def _validate_schema(self, df):
        missing = self.required_columns - set(df.columns)
        if missing:
            raise ValidationError(f"Missing columns: {missing}")

    def _validate_data(self, df):
        if df.isnull().any().any():
            raise ValidationError("Null values detected")

    def _move_to_failed(self, filename):
        src = os.path.join(self.input_path, filename)
        dst = os.path.join(self.failed_path, filename)
        shutil.move(src, dst)

