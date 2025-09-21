import os
import zipfile

def build_project_zip(source_dir=".", output_path="payloads/project_payload.zip"):
    exclude = {"__pycache__", ".git", ".venv", "payloads", "alex_notify_bot_final.zip"}
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            if any(ex in root for ex in exclude):
                continue
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start=source_dir)
                if not any(ex in arcname for ex in exclude):
                    zipf.write(file_path, arcname)

if __name__ == "__main__":
    os.makedirs("payloads", exist_ok=True)
    build_project_zip()
    print("✅ Архив проекта собран: payloads/project_payload.zip")