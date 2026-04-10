import os

import matplotlib.pyplot as plt
import pandas as pd
from django.conf import settings

from app.transaction.models import Transaction

from .models import Analysis


class SpendingAnalyzer:
    def __init__(self, user, period_start, period_end, analysis_type):
        self.user = user
        self.period_start = period_start
        self.period_end = period_end
        self.df = None
        self.image_path = None
        self.analysis_type = analysis_type

    def fetch_data(self):
        transactions = Transaction.objects.filter(
            user=self.user, transaction_type="WITHDRAWAL", created_at__range=(self.period_start, self.period_end)
        ).select_related("account")

        if not transactions.exists():
            raise ValueError("분석할 거래내역이 없습니다.")

        self.df = pd.DataFrame(list(transactions.values("amount", "created_at")))

    def analyze(self):
        self.df["date"] = pd.to_datetime(self.df["created_at"]).dt.date
        self.df["amount"] = self.df["amount"].astype(float)
        self.df = self.df.groupby("date")["amount"].sum().reset_index()

    def visualize(self):
        fig, ax = plt.subplots(figsize=(10, 5))

        ax.bar(self.df["date"].astype(str), self.df["amount"])
        ax.set_title("기간별 지출 분석")
        ax.set_xlabel("날짜")
        ax.set_ylabel("지출 금액 (원)")
        plt.xticks(rotation=45)
        plt.tight_layout()

        save_dir = os.path.join(settings.MEDIA_ROOT, "analysis")
        os.makedirs(save_dir, exist_ok=True)

        filename = f"analysis_{self.user.id}_{self.period_start}_{self.period_end}.png"
        self.image_path = os.path.join("analysis", filename)

        plt.savefig(os.path.join(settings.MEDIA_ROOT, self.image_path))
        plt.close()

    def save(self):
        Analysis.objects.create(
            user=self.user,
            about="총 지출",
            analysis_type=self.analysis_type,
            period_start=self.period_start,
            period_end=self.period_end,
            description=f"{self.period_start} ~ {self.period_end} 기간 총 지출: {self.df['amount'].sum():,.0f}원",
            result_image=self.image_path,
        )

    def run(self):
        self.fetch_data()
        self.analyze()
        self.visualize()
        self.save()
