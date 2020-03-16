#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup
import os

# Здесь можно менять глобальный мажор.минор вашего инструмента.
__version__ = "0.2"
# Итоговая версия после сборки будет выглядеть так:
# [major.minor].[build] для релизных сборок
# и [major.minor.dev]build для нерелизных.

# Билд-статус по умолчанию, смотрите: https://pypi.python.org/pypi?%3Aaction=list_classifiers
devStatus = "2 - Pre-Alpha"

# Логика версионирования в зависимости от веток настраивается ниже:
if "TRAVIS_BUILD_NUMBER" in os.environ and "TRAVIS_BRANCH" in os.environ:
    print("This is TRAVIS-CI build")
    print("TRAVIS_BUILD_NUMBER = {}".format(os.environ["TRAVIS_BUILD_NUMBER"]))
    print("TRAVIS_BRANCH = {}".format(os.environ["TRAVIS_BRANCH"]))

    __version__ += ".{}{}".format(
        "" if "release" in os.environ["TRAVIS_BRANCH"] or os.environ["TRAVIS_BRANCH"] == "master" else "dev",
        os.environ["TRAVIS_BUILD_NUMBER"],
    )

    devStatus = (
        "5 - Production/Stable"
        if "release" in os.environ["TRAVIS_BRANCH"] or os.environ["TRAVIS_BRANCH"] == "master"
        else devStatus
    )
elif "GITLAB_CI" in os.environ:

    print("This is GITLAB-CI build")
    print("CI_PIPELINE_IID = {}".format(os.environ["CI_PIPELINE_IID"]))
    print("CI_COMMIT_BRANCH = {}".format(os.environ["CI_COMMIT_BRANCH"]))

    __version__ += ".{}{}".format(
        "" if "release" in os.environ["CI_COMMIT_BRANCH"] or os.environ["CI_COMMIT_BRANCH"] == "master" else "dev",
        os.environ["CI_PIPELINE_IID"],
    )

    devStatus = (
        "5 - Production/Stable"
        if "release" in os.environ["CI_COMMIT_BRANCH"] or os.environ["CI_COMMIT_BRANCH"] == "master"
        else devStatus
    )
else:
    print("This is local build")
    __version__ += ".dev0"  # set version as major.minor.localbuild if local build: python setup.py install

# Перед сборкой выведется сообщение о том, какая версия собирается
print("XpathWebScrapper build version = {}".format(__version__))

#  Это основной раздел настроек setuptools для сборки вашей программы
setup(
    name="xpathwebscrapper",
    version=__version__,
    # короткое описание проекта - отображается рядом с пакетом в PyPI
    description="Simple and easy configurable web scrapper",
    # подробная документация должна быть доступна в GitHub Pages по этой ссылке
    long_description="About XpathWebScrapper: https://github.com/antonzolotukhin/XpathWebScrapper",
    license="MIT",
    author="Anton Zolotukhin",
    author_email="anton.i.zolotukhin@gmail.com",
    # сюда пишем ссылку на GitHub Pages или другой сайт с документацией
    url="https://github.com/antonzolotukhin/XpathWebScrapper",
    # здесь указываем ссылку на проект в GitHub
    download_url="https://github.com/antonzolotukhin/XpathWebScrapper.git",
    # Точка входа указывает на основной метод, который нужно запустить при запуске программы из консоли.
    # Например, если основной модуль в пакете exampleproject называется Main,
    # то в данном примере будет запущен метод Main() этого скрипта, если вы наберёте в консоли команду "exampleproject"
    entry_points={"console_scripts": ["xpathwebscrapper = xpathwebscrapper.grab:main"]},
    # все допустимые классификаторы для PyPI подробно перечислены на страничке:
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: {}".format(devStatus),
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Russian",
        "Programming Language :: Python :: 3.6",
    ],
    # перечислите все ключевые слова, которые ассоциируются с вашим инструментом, каждое слово отдельной записью
    keywords=["goverenment-data", "lxml", "website-scrapping"],
    # необходимо перечислить ВСЕ каталоги с пакетами, если они присутствуют в вашем проекте, либо оставить '.',
    # что будет указывать на то, что корень проекта сам является пакетом (в корне должен быть __init__.py)
    packages=["xpathwebscrapper"],
    setup_requires=[  # необходимо перечислить ВСЕ библиотеки, от которых зависит сборка вашего инструмента
        "pytest-runner"
    ],
    tests_require=[  # необходимо перечислить ВСЕ библиотеки, которые должны быть установлены для запуска тестов
        "requests",
        "pytest",
        "pytest-cov",
        "pytest-mock",
        "requests-mock",
    ],
    # необходимо перечислить ВСЕ библиотеки, от которых зависит ваш инструмент (requirements),
    # кроме стандартных библиотек, и они будут установлены автоматически при установке вашего инструмента
    install_requires=["lxml", "pandas", "requests", "pyYAML", "certifi"],
    package_data={  # необходимо перечислить ВСЕ файлы, которые должны войти в итоговый пакет, например:
        "": [
            # если проект содержит другие модули, их и все входящие в них файлы тоже нужно перечислить
            "../Examples/*.yml",  # Examples of site definitions
            # все юнит-тесты, если вы хотите, чтобы люди могли их запускать после установки вашей библиотеки
            "../tests/*.py",
            "../LICENSE",  # файл лицензии нужно добавить в пакет
            # '../README.md',  # файл документации нужно добавить в пакет
        ],
    },
    zip_safe=True,
)
