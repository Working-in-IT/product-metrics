# Источники идей

Комплект - самостоятельный формат, собранный по результатам обзора общедоступных подходов. Ссылки дают возможность проверить исходные практики; они не означают совместимость схем или одобрение этого комплекта авторами источников. Дата обзора: 30 сентября 2026 года.

- [GitLab Handbook: Parts of a KPI](https://handbook.gitlab.com/handbook/company/kpis/#parts-of-a-kpi) - смысл, определение, источник и оговорки показателя.
- [GitLab Metrics Dictionary](https://docs.gitlab.com/development/internal_analytics/metrics/metrics_dictionary/) - отдельные структурированные определения, из которых строится каталог.
- [Amplitude Metrics](https://www.amplitude.com/docs/analytics/metrics) - описание, определение, использования и история метрики.
- [OpenMetadata: Metric schema](https://raw.githubusercontent.com/open-metadata/OpenMetadata/main/openmetadata-spec/src/main/resources/json/schema/entity/data/metric.json) - поля метрики и связи с активами. Ссылка ведёт на изменяемую ветку проекта.
- [dbt: Creating metrics](https://docs.getdbt.com/docs/build/metrics-overview) - декларативное описание расчётов, типов метрик и фильтров.
- [Metric Definition Worksheet](https://www.analyticsengineering.com/templates/metric-definition-worksheet) - вопросы к смыслу, формуле и границам метрики.

Ни одна из этих схем не скопирована целиком. Порядок разделов, типы связей, правила версии и разделение переносимого комплекта с местным каталогом - решения данного комплекта. Файлы примеров созданы специально для обучения и не описывают организации из источников.

## Источники версии 0.3.0

Публичные материалы, на которые ссылаются справочники 0.3.0. Ссылки позволяют проверить практики; они не означают одобрения этого комплекта авторами. Правила комплекта, отмеченные как наш вывод, - решения данного комплекта, а не пересказ источников.

### Контрольные карты и вариация

- NIST/SEMATECH - 6.3.2.2. Individuals Control Charts - https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc322.htm
- NIST/SEMATECH - 6.3.2.1. Shewhart X-bar and R and S Control Charts - https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc321.htm
- Wikipedia - Western Electric rules - https://en.wikipedia.org/wiki/Western_Electric_rules
- Stacey Barr - Are You Reacting to Trends That Aren't Really There? - https://web.archive.org/web/20240808171638/https://www.staceybarr.com/downloads/AreYouReactingToTrendsThatArentReallyThere.pdf
- Magdalena Smeds - Exploring Tampering - https://web.archive.org/web/20240520213739/http://liu.diva-portal.org/smash/get/diva2:1639821/FULLTEXT01
- Casas-Arce, Lourenço, Martinez-Jerez - The Performance Effect of Feedback Frequency and Detail - https://web.archive.org/web/20250425160106/https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3005990

### Разложение изменений и диагностика

- Max Halford - Answering "Why did the KPI change?" using decomposition - https://maxhalford.github.io/blog/kpi-evolution-decomposition/
- Paul Levchuk - How to Split a Churn Spike into Mix and Rate - https://medium.com/@paul.levchuk/how-to-split-a-churn-spike-into-mix-and-rate-a-step-by-step-lmdi-guide-6bd813fa70c8
- Sequoia Capital - Analyzing Metric Changes, Part II: Product Changes - https://www.sequoiacap.com/article/product-changes
- Sequoia Capital - Analyzing Metric Changes, Part III: Seasonal Factors - https://www.sequoiacap.com/article/metrics-seasonal-factors
- Sequoia Capital - Analyzing Metric Changes, Part IV: Competition and Other External Factors - https://www.sequoiacap.com/article/metrics-competiton-external-factors
- Sequoia Capital - Analyzing Metric Changes, Part V: Mix Shift - https://articles.sequoiacap.com/metrics-mix-shift
- Sequoia Capital - Analyzing Metric Changes, Part VII: Action Plan - https://www.sequoiacap.com/article/analyzing-metric-changes-part-vii-action-plan
- Uber Engineering - The Journey Towards Metric Standardization - http://web.archive.org/web/20260426041726/https://www.uber.com/us/en/blog/umetric/
- Wu et al. (Pinterest) - The Quest to Understand Metric Movements - https://web.archive.org/web/20250820120557/https://medium.com/pinterest-engineering/the-quest-to-understand-metric-movements-8ab12ae97cda
- Bhagwan et al. - Adtributor - https://www.usenix.org/system/files/conference/nsdi14/nsdi14-paper-bhagwan.pdf
- Kalander - RiskLoc - https://arxiv.org/abs/2205.10004
- Langsrud - ANOVA for unbalanced data: Use Type II instead of Type III sums of squares - http://www.stat.yale.edu/~jtc5/312_612/readings/unbalanced_two-way_anova_and_interactions/unbalanced-anova-use-type-II-SS_Stat-Comput_03.pdf
- Zhao, Mahboobi, Bagheri - Shapley Value Methods for Attribution Modeling in Online Advertising - https://arxiv.org/abs/1804.05327
- Oaxaca, Sierminska - Oaxaca-Blinder meets Kitagawa - https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0321874
- GitLab - KPIs (архив 2021) - https://web.archive.org/web/20210419155110/https://about.gitlab.com/company/kpis/

### Эксперименты и защитные метрики

- Schultzberg, Ankargren, Frånberg (Spotify) - Risk-aware product decisions in A/B tests with multiple metrics - https://arxiv.org/abs/2402.11609
- Schultzberg (Spotify Confidence) - Better Product Decisions with Guardrail Metrics - https://confidence.spotify.com/blog/better-decisions-with-guardrails
- Xifara, Andersen, Yang, Rauh (Airbnb) - Designing Experimentation Guardrails - https://web.archive.org/web/2024/https://medium.com/airbnb-engineering/designing-experimentation-guardrails-ed6a976ec669
- Ishan Goel (Wingify) - Three Kinds of Metrics: The Success, The Guardrail and The Diagnostic - https://wingify.com/blog/three-kinds-of-metrics-the-success-the-guardrail-and-the-diagnostic/
- Kohavi, Longbotham - Online Controlled Experiments and A/B Tests - https://exp-platform.com/Documents/2023-03-11EncyclopeiaMLDSABTestingFinal.pdf
- Chamandy, Muralidharan, Najmi, Naidu (Google) - Estimating Uncertainty for Massive Data Streams - https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/43157.pdf
- Hohnhold, O'Brien, Tang (Google) - Focusing on the Long-term - https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/43887.pdf
- Athey, Chetty, Imbens, Kang - The Surrogate Index - https://www.nber.org/system/files/working_papers/w26463/w26463.pdf

### OKR и обзоры

- John Doerr (What Matters) - OKRs Explained: Inputs, Outputs, & Outcomes - https://www.whatmatters.com/okrs-explained/input-output-outcome-key-results
- Горская (HighTime Media), по Tim Herbig - OKR-методология: как использовать leading и lagging метрики - https://hightime.media/systema-okr/
- Macdonald (OKRs Tool) - 40+ Key Results Examples From Real OKR Data - https://www.okrstool.com/blog/key-results-examples
- Beatriz Boavida (WorkJoy) - An ex-Intel Leader's Guide to OKRs - https://workjoy.co/blog/implement-okrs-as-intel-with-peter-engelbrecht
- Google re:Work - Set goals with OKRs - https://rework.withgoogle.com/intl/en/guides/set-goals-with-okrs
- GitLab Handbook - Objectives and Key Results (архив 2023) - https://web.archive.org/web/2023/https://about.gitlab.com/company/okrs/
- Locke, Latham - Building a Practically Useful Theory of Goal Setting and Task Motivation: A 35-Year Odyssey - https://med.stanford.edu/content/dam/sm/s-spire/documents/PD.locke-and-latham-retrospective_Paper.pdf
- Zhou - A Contemporary Meta-Analysis of Goal Setting and Performance - https://hdl.handle.net/11299/281731
- Spotify HR Blog - Why individual OKRs don't work for us - https://web.archive.org/web/2018/https://hrblog.spotify.com/2016/08/15/our-beliefs/
- Butler, Zimmermann, Bird (Microsoft) - Objectives and Key Results in Software Teams - https://arxiv.org/abs/2311.00236
- Barbala et al. - Objectives and Key Results in Large-Scale Agile Organizations - https://scholarspace.manoa.hawaii.edu/bitstreams/77ad36bd-352f-4ef6-b907-decc14aee9a5/download
- Дудоров (Авито) - Дерево метрик как основа для OKR - https://communities.changeleaders.ru/enterprise-agile-russia/derevo-metrik-kak-osnova-dlya-okr/
- IdeaPlan - North Star Metric vs OKR - https://www.ideaplan.io/compare/okr-vs-north-star-metric
- Cedric Chin (Commoncog) - The Amazon Weekly Business Review - https://commoncog.com/the-amazon-weekly-business-review/
- Cedric Chin (Commoncog) - Amazon's Category Expansion - https://commoncog.com/c/cases/amazon-incentives-category-expansion/
- Cedric Chin (Commoncog) - Goodhart's Law Isn't as Useful as You Might Think - https://commoncog.com/goodharts-law-not-useful/

### Деревья метрик и North Star

- Dillon Baker (Mixpanel) - What is a metric tree? - https://mixpanel.com/blog/metric-tree/
- Syrus Islam - Reconceptualizing the notion of relations underlying performance measurement models - https://openrepository.aut.ac.nz/bitstreams/9cf3f3f4-52c6-4595-b20b-890fcdb25f02/download
- Lenny Rachitsky - Choosing Your North Star Metric - https://future.com/north-star-metrics/
- Ravi Mehta - Your product team doesn't need a "North Star Metric" - https://web.archive.org/web/20250404031212/https://blog.ravi-mehta.com/p/your-product-team-doesnt-need-a-north
- Balfour, Clowes, Winters (Reforge) - Don't Let Your North Star Metric Deceive You - https://web.archive.org/web/20180824194122/https://www.reforge.com/blog/north-star-metric-growth
- Amplitude - The North Star Playbook - https://info.amplitude.com/rs/138-CDN-550/images/Amplitude-The-North-Star-Playbook.pdf
- Rodden, Hutchinson, Fu (Google) - Measuring the User Experience on a Large Scale - https://research.google.com/pubs/archive/36299.pdf
- Heap - Building a Retention Strategy, Part 2 - https://www.heap.io/blog/building-a-retention-strategy-part-2-connecting-activities
- Andrew Chen - What to do when product growth stalls - https://andrewchen.com/growth-stalls/
- Jonathan Hsu - Diligence at Social Capital Part 1: Accounting for User Growth - https://web.archive.org/web/2023/https://medium.com/swlh/diligence-at-social-capital-part-1-accounting-for-user-growth-4a8a449fddfc
- Tribe Capital - A Quantitative Approach to Product Market Fit - https://tribecap.co/essays/a-quantitative-approach-to-product-market-fit
- Tribe Capital - Unit Economics and the Pursuit of Scale Invariance - https://tribecap.co/essays/unit-economics-and-the-pursuit-of-scale-invariance
- Sean Ellis - Using Product/Market Fit to Drive Sustainable Growth - https://web.archive.org/web/2020/https://medium.com/growthhackers/using-product-market-fit-to-drive-sustainable-growth-58e9124ee8db
- David Skok - SaaS Metrics 2.0 - https://www.forentrepreneurs.com/saas-metrics-2/
- Byron Deeter (Bessemer) - The five accounting metrics for cloud companies - https://www.bvp.com/atlas/cloud-computing-metrics
- Chang et al. (Airbnb) - How Airbnb achieved metric consistency at scale, Part I: Minerva - http://web.archive.org/web/20260809070448/https://medium.com/airbnb-engineering/how-airbnb-achieved-metric-consistency-at-scale-f23cc53dea70
- Robert Kaplan - Conceptual Foundations of the Balanced Scorecard (HBS 10-074) - https://www.hbs.edu/ris/Publication%20Files/10-074_0bf3c151-f82b-4592-b885-cdde7f5d97a6.pdf
- Quesado, Aibar Guzmán, Lima Rodrigues - O Tableau de Bord e o Balanced Scorecard - https://revistas.ufpr.br/rcc/article/download/28110/19291/108918
- Onetribe - KPI Hierarchies and Cascading - https://www.onetribeadvisory.com/knowledge-hub/kpi-hierarchies-cascading/
- KPI Tree - North Star Framework vs Metric Trees - https://kpitree.co/guides/frameworks/north-star-framework-vs-metric-trees
- IdeaPlan - The Product Metrics Handbook - https://www.ideaplan.io/metrics-guide/read
- David Parmenter - Key Performance Indicators (4th ed.), PDF Toolkit - https://davidparmenter.com/wp-content/uploads/2024/10/Key-Performance-Indicators-4th-edition-PDF-Toolkit.pdf
- Eric Ries - Why vanity metrics are dangerous - https://www.startuplessonslearned.com/2009/12/why-vanity-metrics-are-dangerous.html
- Eric Ries - Entrepreneurs: Beware of Vanity Metrics (Harvard Business Review) - https://hbr.org/2010/02/entrepreneurs-beware-of-vanity-metrics
- Keiningham et al. - A Longitudinal Examination of Net Promoter and Firm Revenue Growth - https://www.deep-insight.com/wp-content/uploads/2018/12/Longitudinal-Examination-of-Net-Promoter-Journal-of-Marketing-Jul-2007.pdf
- Frederick Reichheld - The One Number You Need to Grow (Harvard Business Review) - https://hbr.org/2003/12/the-one-number-you-need-to-grow

### Дашборды

- Stephen Few - Common Pitfalls in Dashboard Design - https://www.perceptualedge.com/articles/Whitepapers/Common_Pitfalls.pdf
- Klipfolio - 4 types of dashboards - https://www.klipfolio.com/blog/starter-guide-to-dashboards
- Working Backwards - Input Metrics for Business Growth - https://workingbackwards.com/concepts/input-metrics/
- Jakob Nielsen - Thinking Aloud: The #1 Usability Tool - https://www.nngroup.com/articles/thinking-aloud-the-1-usability-tool/
