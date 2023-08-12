from typing import Annotated

import numpy as np
import soundfile as sf
from drmeter.algorithm import dynamic_range
from drmeter.models import AudioData
from fastapi import FastAPI, File, HTTPException, UploadFile

from drmeter_web.models import AnalysisResponse, AnalysisResult, RawAudio

app = FastAPI(
    title="Dynamic Range (DR) Analysis API",
    docs_url="/",
)


@app.post(
    "/analyze/file",
    response_model=AnalysisResponse,
    name="Analyze audiofile",
)
def analyze_file(
    file: Annotated[UploadFile, File(description="An audiofile to analyze")],
) -> AnalysisResponse:
    try:
        with sf.SoundFile(file.file) as soundfile:
            dr = dynamic_range(AudioData.from_soundfile(soundfile))
            return AnalysisResponse(
                result=AnalysisResult.from_dr_result(dr),
                filename=file.filename,
                frames=soundfile.frames,
                channels=soundfile.channels,
                samplerate=soundfile.samplerate,
            )
    except sf.SoundFileError as exc:
        raise HTTPException(status_code=400, detail="Could not analyze file") from exc


@app.post(
    "/analyze/raw",
    response_model=AnalysisResponse,
    name="Analyze raw sample data",
)
def analyze_raw(
    raw: RawAudio,
) -> AnalysisResponse:
    try:
        data = AudioData(
            data=np.asarray(raw.data, dtype=np.float64),
            samplerate=raw.samplerate,
            frames=len(raw.data),
            channels=len(raw.data[0]),
        )

        dr = dynamic_range(data)
        return AnalysisResponse(
            result=AnalysisResult.from_dr_result(dr),
            samplerate=data.samplerate,
            frames=data.frames,
            channels=data.channels,
        )
    except sf.SoundFileError as exc:
        raise HTTPException(status_code=400, detail="Could not analyze file") from exc
