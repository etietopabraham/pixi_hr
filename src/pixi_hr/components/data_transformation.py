import os
import pandas as pd
from sklearn.model_selection import train_test_split
from pixi_hr import logger
from sklearn.preprocessing import LabelEncoder
import re
from sklearn.preprocessing import MultiLabelBinarizer
import ast


from pixi_hr.config.configuration import DataTransformationConfig

class DataTransformation:
    """
    DataTransformation class for transforming the raw data into a machine learning ready format.
    
    Attributes:
    - config (DataTransformationConfig): Configuration object containing paths.
    - df (DataFrame): Pandas DataFrame loaded from the specified data file.
    """
    
    def __init__(self, config: DataTransformationConfig):
        """
        Initializes the DataTransformation class.

        Args:
        - config (DataTransformationConfig): Configuration object containing paths.
        """
        self.config = config

        try:
            # Load the data into a DataFrame
            self.df = pd.read_csv(self.config.data_path)
        except FileNotFoundError:
            logger.error(f"File not found: {self.config.data_path}")
            raise
        except Exception as e:
            logger.error(f"Error reading data file: {e}")
            raise


    def clean_skills(self, skill_list_str):
        """Clean the skills from the job_qualifications column."""
        try:
            # Safely evaluate the string as a Python expression
            skill_list = ast.literal_eval(skill_list_str)

            if not isinstance(skill_list, list):
                raise ValueError("Input is not a list")

            # Clean each skill
            cleaned_skills = []
            for skill in skill_list:
                cleaned_skill = skill.strip().lower()  # Convert to lowercase and remove leading/trailing whitespaces
                cleaned_skill = re.sub(r'[^a-z0-9]', '', cleaned_skill)  # Remove special characters
                cleaned_skills.append(cleaned_skill)

            return cleaned_skills
        except (ValueError, SyntaxError):
            # Handle invalid input gracefully
            return []
    
    def one_hot_encode_qualifications(self):
        """One-hot encodes the job qualifications."""
        # Clean the skills
        self.df['job_qualifications'] = self.df['job_qualifications'].apply(self.clean_skills)

        # Initialize the MultiLabelBinarizer
        mlb = MultiLabelBinarizer()

        # One-hot encode the cleaned skills
        encoded_qualifications = mlb.fit_transform(self.df['job_qualifications'])

        # Add a prefix to the encoded column names
        encoded_columns = [f"qual_{col}" for col in mlb.classes_]

        # Convert the one-hot encoded skills into a DataFrame
        encoded_df = pd.DataFrame(encoded_qualifications, columns=encoded_columns)

        # Drop the original job_qualifications column and concat the encoded DataFrame
        self.df = pd.concat([self.df.drop('job_qualifications', axis=1), encoded_df], axis=1)

        logger.info("One-hot encoding of job qualifications completed.")


    
    def datetime_conversion_and_extraction(self):
        """
        Convert the date_of_job_post column into a datetime format and extract
        year, month, day, hour, minute, and second as separate columns.
        """
        self.df['date_of_job_post'] = pd.to_datetime(self.df['date_of_job_post'])
        
        # Extracting different datetime features
        self.df['month_of_job_post'] = self.df['date_of_job_post'].dt.month
        self.df['day_of_job_post'] = self.df['date_of_job_post'].dt.day
        self.df['year_of_job_post'] = self.df['date_of_job_post'].dt.year
        self.df['hour_of_job_post'] = self.df['date_of_job_post'].dt.hour
        self.df['minute_of_job_post'] = self.df['date_of_job_post'].dt.minute
        self.df['second_of_job_post'] = self.df['date_of_job_post'].dt.second

        logger.info("Datetime conversion and feature extraction completed.")
    
   
    def categorical_encoding(self):
        """
        Convert categorical columns to numerical format using label encoding.
        """
        label_encoders = {}  # Store the encoders for potential use later
        for col in ['title', 'job_location', 'company_name', 'job_type']:
            le = LabelEncoder()
            self.df[col] = le.fit_transform(self.df[col])
            label_encoders[col] = le
        logger.info("Categorical encoding completed.")

    
    def handle_missing_values(self):
        """
        Handle missing values in the specified columns by dropping them.
        """
        # self.df.dropna(subset=['job_qualifications', 'job_type', 'job_location'], inplace=True)
        self.df.dropna()
        logger.info("Handling of missing values completed.")

    
    def split_data(self):
        """
        Split the data into train and test sets and save them to respective paths.
        """
        train, test = train_test_split(self.df, test_size=0.2, random_state=44)

        train.to_csv(os.path.join(self.config.root_dir, 'train_data.csv'), index=False)
        test.to_csv(os.path.join(self.config.root_dir, 'test_data.csv'), index=False)

        logger.info("Data split into train and test sets and saved to respective paths.")
        logger.info(f"Train shape: {train.shape}")
        logger.info(f"Test shape: {test.shape}")

        print(f"Train shape: {train.shape}")
        print(f"Test shape: {test.shape}")

    
    def main(self):
        """
        Orchestrates the sequence of data transformations.
        """
        logger.info("Starting Data Transformation...")
        
        # Step 1: Datetime Conversion and Feature Extraction
        logger.info("Datetime Conversion and Feature Extraction...")
        self.datetime_conversion_and_extraction()

        # Step 2: Categorical Encoding
        logger.info("Categorical Encoding...")
        self.categorical_encoding()

        # Step 3: Handling Missing Values
        logger.info("Handling Missing Values...")
        self.handle_missing_values()

        # Step 4: One-Hot Encoding of Job Qualifications
        logger.info("One-Hot Encoding of Job Qualifications...")
        self.one_hot_encode_qualifications()

        # Step 5: Split Data into Train and Test sets
        logger.info("Splitting Data...")
        self.split_data()

        logger.info("Data Transformation completed successfully.")