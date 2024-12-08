import os
import json
from analyze.model.domain.observation import Observation
from analyze.repository.observation import ObservationRepository
from analyze.exception import ObservationNotFound


class ObservationService:

    def __init__(self, observation_repository: ObservationRepository):
        self.observation_repository = observation_repository

    def get(self, id: str) -> Observation:
        observation = self.observation_repository.get(id)
        if observation is None:
            raise ObservationNotFound(id)
        return observation

    def list(self) -> list[Observation]:
        if len(self.observation_repository.list()) == 0:
            raise ObservationNotFound(-1)
        return self.observation_repository.list()
