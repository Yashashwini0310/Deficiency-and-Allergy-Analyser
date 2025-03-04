import os
import zipfile

def create_lambda_package():
    lambda_dir = "lambda_code"
    zip_file = "lambda_function.zip"

    # Create ZIP file
    with zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(lambda_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, lambda_dir))

    print(f"Lambda function zipped successfully! {zip_file}")

if __name__ == "__main__":
    create_lambda_package()