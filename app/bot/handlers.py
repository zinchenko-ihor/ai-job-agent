from __future__ import annotations

import asyncio

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from app.bot.keyboards import main_keyboard

from app.db.session import SessionLocal

from app.services.job_collection import (
    JobCollectionService,
)

from app.services.job_recommendation import (
    JobRecommendationService,
)


router = Router()



# =====================================================
# START
# =====================================================

@router.message(CommandStart())
async def start_handler(
    message: Message,
):

    await message.answer(
        "Привіт! 👋\n\n"
        "Я AI Job Agent 🤖\n\n"
        "Я допоможу знайти релевантні вакансії "
        "під твій досвід.\n\n"
        "Що потрібно зробити:\n\n"
        "1️⃣ Надішли резюме PDF\n"
        "2️⃣ Я проаналізую твій профіль\n"
        "3️⃣ Знайду актуальні вакансії DOU\n"
        "4️⃣ Відсортую їх за відповідністю\n\n"
        "Після аналізу CV натисни 🔎 Вакансії",
        reply_markup=main_keyboard(),
    )



# =====================================================
# JOB SEARCH
# =====================================================

@router.message(Command("jobs"))
@router.message(
    lambda message:
    message.text == "🔎 Вакансії"
)
async def jobs_handler(
    message: Message,
):

    await message.answer(
        "🔎 Оновлюю вакансії DOU та "
        "аналізую відповідність..."
    )


    session = SessionLocal()


    try:

        # ---------------------------------------------
        # 1. Update DOU vacancies
        # ---------------------------------------------

        collector = JobCollectionService(
            session
        )


        collection_result = await asyncio.to_thread(
            collector.collect_dou,
            "devops",
        )


        print(
            "DOU UPDATE:",
            collection_result,
        )



        # ---------------------------------------------
        # 2. Generate recommendations
        # ---------------------------------------------

        recommendation_service = (
            JobRecommendationService(
                session
            )
        )


        recommendations = (
            recommendation_service
            .get_recommendations(
                user_id=message.from_user.id,
                limit=5,
                force_refresh=True,
            )
        )



        if not recommendations:

            await message.answer(
                "😔 Не знайдено релевантних вакансій.\n\n"
                "Перевір, чи завантажене резюме."
            )

            return



        # ---------------------------------------------
        # 3. Telegram response
        # ---------------------------------------------

        text = (
            "🔥 Топ вакансій для тебе:\n\n"
        )


        for index, item in enumerate(
            recommendations,
            start=1,
        ):


            text += (
                f"{index}. {item['title']}\n"
                f"🏢 {item['company']}\n"
                f"📍 {item.get('location','')}\n"
                f"⭐ Match: {item['score']}%\n"
                f"💡 {item['reason']}\n"
                f"🔗 {item['url']}\n\n"
            )


        await message.answer(
            text,
            disable_web_page_preview=True,
            reply_markup=main_keyboard(),
        )


    except Exception as exc:

        print(
            "ERROR /jobs:",
            exc,
        )


        await message.answer(
            "❌ Не вдалося отримати вакансії."
        )


    finally:

        session.close()



# =====================================================
# FORCE DOU UPDATE
# =====================================================

@router.message(
    lambda message:
    message.text == "🔄 Оновити вакансії"
)
async def refresh_jobs_handler(
    message: Message,
):

    await message.answer(
        "🔄 Завантажую свіжі вакансії DOU..."
    )


    session = SessionLocal()


    try:

        collector = JobCollectionService(
            session
        )


        result = await asyncio.to_thread(
            collector.collect_dou,
            "devops",
        )


        await message.answer(
            "✅ DOU оновлено:\n\n"
            f"📥 Отримано: {result['fetched']}\n"
            f"🟢 Свіжі: {result['fresh']}\n"
            f"➕ Додано: {result['created']}\n"
            f"♻️ Існуючі: {result['existing']}",
            reply_markup=main_keyboard(),
        )


    except Exception as exc:

        print(
            "ERROR refresh jobs:",
            exc,
        )


        await message.answer(
            "❌ Помилка оновлення вакансій."
        )


    finally:

        session.close()



# =====================================================
# PROFILE
# =====================================================

@router.message(
    lambda message:
    message.text == "👤 Мій профіль"
)
async def profile_handler(
    message: Message,
):

    session = SessionLocal()


    try:

        service = JobRecommendationService(
            session
        )


        profile = (
            service.profile_repository
            .get(
                message.from_user.id
            )
        )


        if not profile:

            await message.answer(
                "📄 Резюме ще не завантажено."
            )

            return



        await message.answer(
            "👤 Твій профіль:\n\n"
            f"Ім'я: {profile.get('name')}\n"
            f"Рівень: {profile.get('seniority')}\n"
            f"English: {profile.get('english_level')}\n\n"
            "Цільові ролі:\n"
            +
            "\n".join(
                profile.get(
                    "target_roles",
                    []
                )
            ),
            reply_markup=main_keyboard(),
        )


    except Exception as exc:

        print(
            "ERROR profile:",
            exc,
        )


        await message.answer(
            "❌ Не вдалося отримати профіль."
        )


    finally:

        session.close()



# =====================================================
# CLEAR
# =====================================================

@router.message(Command("clear"))
@router.message(
    lambda message:
    message.text == "🧹 Очистити"
)
async def clear_handler(
    message: Message,
):

    await message.answer(
        "🧹 Діалог очищено.",
        reply_markup=main_keyboard(),
    )
