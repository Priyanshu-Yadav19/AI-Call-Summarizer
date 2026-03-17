import os
import time
import json
import mimetypes
import requests
from datetime import datetime

from app.config import settings


class SarvamSTT:
    def __init__(self) -> None:
        print("Initializing Sarvam Batch STT...")

        self.api_key = settings.SARVAM_API_KEY
        if not self.api_key:
            raise ValueError("SARVAM_API_KEY is missing")

        self.model = settings.SARVAM_MODEL
        self.transcript_dir = settings.TRANSCRIPT_DIR
        os.makedirs(self.transcript_dir, exist_ok=True)

        self.headers = {
            "api-subscription-key": self.api_key,
            "Content-Type": "application/json",
        }

        self.base_url = "https://api.sarvam.ai/speech-to-text/job/v1"

        print("Sarvam Batch STT initialized.")

    def transcribe(self, audio_path: str) -> str:
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        print("Starting batch transcription...")

        file_name = os.path.basename(audio_path)

        job_id = self._create_job()
        upload_url = self._get_upload_url(job_id, file_name)
        self._upload_file(upload_url, audio_path)
        self._start_job(job_id)

        result = self._poll_job(job_id)
        transcript = self._extract_transcript(job_id, result)

        if not transcript:
            transcript = "No speech detected."

        path = self._save_transcript_file(audio_path, transcript)
        print(f"Transcript saved: {path}")

        return transcript

    def _create_job(self) -> str:
        payload = {
            "job_parameters": {
                "model": self.model
            }
        }

        res = requests.post(self.base_url, json=payload, headers=self.headers)
        print("Create job response:", res.status_code, res.text)
        res.raise_for_status()

        data = res.json()
        job_id = data["job_id"]
        print(f"Job created: {job_id}")
        return job_id

    def _get_upload_url(self, job_id: str, file_name: str) -> str:
        url = f"{self.base_url}/upload-files"

        payload = {
            "job_id": job_id,
            "files": [file_name],
        }

        res = requests.post(url, json=payload, headers=self.headers)
        print("Upload URL response:", res.status_code, res.text)
        res.raise_for_status()

        data = res.json()
        print("Upload URL parsed JSON:", data)

        upload_urls = data.get("upload_urls")
        if not upload_urls:
            raise ValueError("No upload_urls returned from Sarvam.")

        if isinstance(upload_urls, dict):
            entry = upload_urls.get(file_name)

            if entry is None:
                available = list(upload_urls.keys())
                raise ValueError(
                    f"Upload URL not returned for file: {file_name}. Available keys: {available}"
                )

            if isinstance(entry, dict):
                upload_url = entry.get("file_url") or entry.get("url")
            else:
                upload_url = entry

            if upload_url and isinstance(upload_url, str):
                return upload_url.strip()

        if isinstance(upload_urls, list):
            for item in upload_urls:
                if not isinstance(item, dict):
                    continue
                if item.get("file_name") == file_name:
                    upload_url = item.get("file_url") or item.get("url")
                    if upload_url:
                        return upload_url.strip()

        raise ValueError(f"Could not extract upload URL for file: {file_name}")

    def _upload_file(self, upload_url: str, audio_path: str) -> None:
        content_type = mimetypes.guess_type(audio_path)[0] or "application/octet-stream"
        file_size = os.path.getsize(audio_path)

        upload_headers = {
            "x-ms-blob-type": "BlockBlob",
            "Content-Type": content_type,
            "Content-Length": str(file_size),
        }

        with open(audio_path, "rb") as f:
            res = requests.put(upload_url, data=f, headers=upload_headers)
            print("File upload response:", res.status_code, res.text)
            res.raise_for_status()

        print("File uploaded successfully.")

    def _start_job(self, job_id: str) -> None:
        url = f"{self.base_url}/{job_id}/start"

        res = requests.post(
            url,
            headers={"api-subscription-key": self.api_key}
        )
        print("Start job response:", res.status_code, res.text)
        res.raise_for_status()

        print("Job started.")

    def _poll_job(self, job_id: str) -> dict:
        url = f"{self.base_url}/{job_id}/status"

        print("Polling job status...")

        while True:
            res = requests.get(
                url,
                headers={"api-subscription-key": self.api_key}
            )
            print("Status response:", res.status_code, res.text)
            res.raise_for_status()

            data = res.json()
            job_state = data.get("job_state")
            print(f"Job state: {job_state}")

            if job_state == "Completed":
                return data

            if job_state == "Failed":
                raise ValueError(data.get("error_message") or "Batch STT job failed.")

            time.sleep(3)

    def _extract_transcript(self, job_id: str, data: dict) -> str:
        job_details = data.get("job_details") or []
        if not job_details:
            return ""

        first = job_details[0]
        outputs = first.get("outputs") or []
        if not outputs:
            return ""

        output_file = outputs[0]
        file_name = output_file.get("file_name")
        if not file_name:
            return ""

        print(f"Preparing download link for result file: {file_name}")

        # Step 1: get presigned download URL from Sarvam
        download_link_url = f"{self.base_url}/download-files"
        payload = {
            "job_id": job_id,
            "files": [file_name],
        }

        res = requests.post(download_link_url, json=payload, headers=self.headers)
        print("Download links response:", res.status_code, res.text)
        res.raise_for_status()

        download_data = res.json()
        download_urls = download_data.get("download_urls")
        if not download_urls:
            raise ValueError("No download_urls returned from Sarvam.")

        result_url = None

        if isinstance(download_urls, dict):
            entry = download_urls.get(file_name)
            if isinstance(entry, dict):
                result_url = entry.get("file_url") or entry.get("url")
            else:
                result_url = entry

        if isinstance(download_urls, list) and not result_url:
            for item in download_urls:
                if not isinstance(item, dict):
                    continue
                if item.get("file_name") == file_name:
                    result_url = item.get("file_url") or item.get("url")
                    break

        if not result_url:
            raise ValueError(f"Could not extract download URL for file: {file_name}")

        # Step 2: fetch actual result JSON from returned URL
        result_res = requests.get(result_url)
        print("Result file fetch response:", result_res.status_code)
        result_res.raise_for_status()

        try:
            result_json = result_res.json()
        except Exception:
            print("Raw result text:", result_res.text[:1000])
            raise ValueError("Downloaded result file is not valid JSON.")

        print("Result JSON:", result_json)

        # Common transcript shapes
        if isinstance(result_json, dict):
            if isinstance(result_json.get("transcript"), str):
                return result_json["transcript"].strip()

            if isinstance(result_json.get("text"), str):
                return result_json["text"].strip()

            if isinstance(result_json.get("results"), list):
                texts = []
                for item in result_json["results"]:
                    if isinstance(item, dict):
                        text = item.get("text")
                        if isinstance(text, str) and text.strip():
                            texts.append(text.strip())
                if texts:
                    return " ".join(texts)

            if isinstance(result_json.get("segments"), list):
                texts = []
                for seg in result_json["segments"]:
                    if isinstance(seg, dict):
                        text = seg.get("text")
                        if isinstance(text, str) and text.strip():
                            texts.append(text.strip())
                if texts:
                    return " ".join(texts)

        return json.dumps(result_json, ensure_ascii=False, indent=2)

    def _save_transcript_file(self, audio_path: str, transcript: str) -> str:
        base = os.path.splitext(os.path.basename(audio_path))[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(self.transcript_dir, f"{base}_{timestamp}.txt")

        with open(path, "w", encoding="utf-8") as f:
            f.write(transcript)

        return path