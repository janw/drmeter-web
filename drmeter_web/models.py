from __future__ import annotations

import numpy as np
from drmeter.models import DynamicRangeResult
from pydantic import BaseModel, computed_field

RESULT_PRECISION = 2


class AnalysisResult(BaseModel):
    per_channel_dr_score: list[float]
    per_channel_peak_db: list[float]
    per_channel_rms_db: list[float]

    overall_dr_score: float
    overall_peak_db: float
    overall_rms_db: float

    @classmethod
    def from_dr_result(cls, dr: DynamicRangeResult) -> AnalysisResult:
        return cls(
            per_channel_dr_score=np.round(
                dr.dr_score.tolist(),
                decimals=RESULT_PRECISION,
            ),
            per_channel_peak_db=np.round(
                dr.peak_db.tolist(),
                decimals=RESULT_PRECISION,
            ),
            per_channel_rms_db=np.round(
                dr.rms_db.tolist(),
                decimals=RESULT_PRECISION,
            ),
            overall_dr_score=round(
                dr.overall_dr_score,
                ndigits=RESULT_PRECISION,
            ),
            overall_peak_db=round(
                dr.overall_peak_db,
                ndigits=RESULT_PRECISION,
            ),
            overall_rms_db=round(
                dr.overall_rms_db,
                ndigits=RESULT_PRECISION,
            ),
        )


class AnalysisResponse(BaseModel):
    filename: str | None = None
    samplerate: int
    frames: int
    channels: int

    result: AnalysisResult

    @computed_field  # type: ignore[misc]
    @property
    def duration(self) -> float:
        return round(self.frames / self.samplerate, RESULT_PRECISION)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "filename": "file_to_analyze.wav",
                    "samplerate": 44100,
                    "frames": 19667756,
                    "channels": 2,
                    "duration": 445.98,
                    "result": {
                        "overall_dr_score": 11.4,
                        "overall_peak_db": -3.53,
                        "overall_rms_db": -19.29,
                        "per_channel_dr_score": [11.23, 11.57],
                        "per_channel_peak_db": [-3.53, -4.53],
                        "per_channel_rms_db": [-18.86, -19.75],
                    },
                }
            ]
        }
    }


class RawAudio(BaseModel):
    data: list[list[float]]
    samplerate: int
