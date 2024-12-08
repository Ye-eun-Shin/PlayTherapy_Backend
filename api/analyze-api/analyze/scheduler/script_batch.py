import warnings

warnings.filterwarnings("ignore")

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.base import STATE_RUNNING
from analyze.container import Container
from dependency_injector.wiring import inject, Provide

from analyze.service.analyze import AnalyzeService

sched = BackgroundScheduler(timezone="Asia/Seoul")


@sched.scheduled_job("cron", second="0", id="analyze")
@inject
def analyze_job(
    analyze_service: AnalyzeService = Provide[Container.analyze_service],
):
    print("Analyze start!")
    analyze_service.run_from_db()


def start_analyze():
    sched.start()


def stop_analyze():
    sched.remove_job("analyze")
    if sched.state == STATE_RUNNING:
        sched.shutdown()
