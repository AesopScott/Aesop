# The Ladder Products Catalog

Last researched: 2026-06-09

Purpose: curriculum backbone for a live `/theladder-products` page. The product track teaches learners how to use the AI products they are most likely to meet at work, school, and in public life.

## Selection Method

There is no single public source that can honestly prove the "250 most used products with AI" across consumer apps, enterprise suites, developer tools, infrastructure, healthcare, legal, security, education, and creative work. This catalog uses a weighted selection method:

- Consumer usage signal: products appearing in high-traffic and high-mobile-use AI app lists, especially a16z's Top 100 Gen AI Consumer Apps.
- Enterprise adoption signal: tools named in workplace AI adoption surveys and business spending/adoption reports.
- Ecosystem importance: products that are common integration targets or infrastructure layers for RAG, agents, analytics, and AI application development.
- Curriculum value: products that represent an important product type learners need to understand, even when usage is split across many similar vendors.

Course depth:

- `B`: beginner course only.
- `B/I`: beginner and intermediate.
- `B/I/A`: beginner, intermediate, and advanced.

## Research Sources

- a16z, [The Top 100 Gen AI Consumer Apps - 6th Edition](https://a16z.com/100-gen-ai-apps-6/)
- Ramp, [AI Index April 2026 update](https://ramp.com/leading-indicators/april-2026-ai-index)
- Wharton Human-AI Research and GBK Collective, [2025 AI Adoption Report](https://ai.wharton.upenn.edu/wp-content/uploads/2025/10/2025-Wharton-GBK-AI-Adoption-Report_Full-Report.pdf)
- OpenAI, [The state of enterprise AI 2025 report](https://openai.com/business/guides-and-resources/the-state-of-enterprise-ai-2025-report/)
- World Bank, [Who on Earth Is Using Generative AI? Global Trends and Shifts in 2025](https://documents1.worldbank.org/curated/en/099856110152535288/pdf/IDU-42736e6b-48fb-45e6-8638-cec68a650f40.pdf)
- Similarweb/Semrush-derived public rankings, used only as directional traffic signals where primary usage data is unavailable.

## Curriculum Categories

The 500 products are separated into these curriculum blocks:

| Rows | Curriculum Block | Count |
|---:|---|---:|
| 1-20 | General AI assistants and answer engines | 20 |
| 21-35 | Workplace productivity, writing, and project tools | 15 |
| 36-61 | Coding, app building, and developer tools | 26 |
| 62-82 | Search, research, knowledge, and RAG applications/frameworks | 21 |
| 83-107 | Databases, vector stores, and managed RAG infrastructure | 25 |
| 108-126 | Data analysis, BI, analytics, and ML platforms | 19 |
| 127-146 | Image, design, and presentation tools | 20 |
| 147-166 | Video, audio, voice, and meeting tools | 20 |
| 167-191 | Go-to-market, CRM, marketing, and customer support | 25 |
| 192-210 | Automation, agents, and workflow builders | 19 |
| 211-230 | Model APIs, cloud AI platforms, and inference infrastructure | 20 |
| 231-250 | Regulated and vertical AI: legal, health, finance, security | 20 |
| 251-275 | HR, recruiting, and talent intelligence | 25 |
| 276-300 | Education, tutoring, and classroom AI | 25 |
| 301-325 | Ecommerce, retail, and merchandising AI | 25 |
| 326-350 | Finance, accounting, FP&A, procurement, and tax | 25 |
| 351-375 | AIOps, observability, and incident response | 25 |
| 376-400 | AI governance, model risk, privacy, and compliance | 25 |
| 401-425 | Architecture, construction, and real estate | 25 |
| 426-450 | Manufacturing, supply chain, logistics, and industrial AI | 25 |
| 451-475 | Scientific, biotech, lab, and clinical AI | 25 |
| 476-500 | Personal productivity, notes, email, calendar, and knowledge AI | 25 |

| # | Product | Product Type | Why It Belongs | Course Depth |
|---:|---|---|---|---|
| 1 | ChatGPT | General AI assistant | Largest mainstream AI assistant and a core reference product for prompting, files, images, voice, agents, and analysis. | B/I/A |
| 2 | Claude | General AI assistant | Major workplace assistant, strong in writing, analysis, long context, coding, and enterprise workflows. | B/I/A |
| 3 | Google Gemini | General AI assistant | Deeply distributed through Google Search, Android, Workspace, and cloud products. | B/I/A |
| 4 | Microsoft Copilot | General AI assistant | Broad default AI entry point across Windows, Edge, Bing, and Microsoft accounts. | B/I/A |
| 5 | Perplexity | Answer engine | Popular AI search and citation workflow; useful for research literacy and verification. | B/I/A |
| 6 | Meta AI | General AI assistant | Embedded across Facebook, Instagram, WhatsApp, and Messenger, creating massive casual usage. | B/I |
| 7 | Grok | General AI assistant | Important X-native assistant with real-time social context and developer ecosystem relevance. | B/I |
| 8 | DeepSeek | General AI assistant | High-usage global assistant and model ecosystem, important for cost, open-weight, and reasoning comparisons. | B/I/A |
| 9 | Poe | Multi-model assistant | Teaches model comparison, bot marketplaces, and user-facing multi-model routing. | B/I |
| 10 | Character.AI | Companion/chat product | One of the defining consumer AI companion products and roleplay/chat pattern references. | B/I |
| 11 | Pi | Personal AI assistant | Important conversational coaching and supportive-assistant pattern. | B |
| 12 | You.com | AI search assistant | Search, chat, and research product with a long-running AI search footprint. | B/I |
| 13 | Phind | Developer search assistant | Strong developer search and answer workflow for technical troubleshooting. | B/I |
| 14 | Kimi | General AI assistant | Widely used Chinese-market assistant known for long-context document work. | B/I |
| 15 | Doubao | General AI assistant | ByteDance assistant with major China-market consumer adoption. | B/I |
| 16 | Qwen Chat | General AI assistant | Alibaba model app and ecosystem entry point for global open-model literacy. | B/I |
| 17 | Le Chat by Mistral | General AI assistant | European AI assistant tied to Mistral's model ecosystem and enterprise positioning. | B/I |
| 18 | HuggingChat | Open model assistant | Teaches open-model assistants, community models, and Hugging Face workflows. | B/I |
| 19 | Luzia | WhatsApp AI assistant | Large messaging-native assistant, useful for teaching mobile and chat-distributed AI. | B |
| 20 | Genspark | Agentic search assistant | Popular agentic research/search product and bridge to autonomous task workflows. | B/I |
| 21 | Microsoft 365 Copilot | Office productivity suite | The most important enterprise AI suite for Word, Excel, PowerPoint, Outlook, and Teams. | B/I/A |
| 22 | Gemini for Google Workspace | Office productivity suite | Core AI layer for Docs, Sheets, Slides, Gmail, Meet, and Drive. | B/I/A |
| 23 | Notion AI | Workspace/document assistant | Common knowledge-work AI product for notes, docs, databases, and team wikis. | B/I |
| 24 | Grammarly | Writing assistant | One of the most-used AI writing and communication products. | B/I |
| 25 | QuillBot | Writing and paraphrasing assistant | High-usage student and professional writing tool for paraphrase, grammar, and summarization. | B |
| 26 | Wordtune | Writing assistant | Useful for tone, rewrite, and workplace communication instruction. | B |
| 27 | Jasper | Marketing writing platform | Mature AI writing platform for brand voice, campaigns, and content teams. | B/I |
| 28 | Copy.ai | Marketing writing and workflow platform | Teaches GTM workflows, content generation, and sales/marketing automation patterns. | B/I |
| 29 | Writesonic | Content and SEO writing platform | Popular marketing copy, blog, and SEO generation tool. | B/I |
| 30 | Writer | Enterprise writing platform | Enterprise-grade writing, governance, brand voice, and custom AI apps. | B/I/A |
| 31 | Sudowrite | Creative writing assistant | Important fiction and creative writing AI product. | B/I |
| 32 | Coda AI | Docs and team workspace | Shows AI inside collaborative docs, tables, and lightweight apps. | B/I |
| 33 | ClickUp Brain | Project management AI | Common project-management AI for tasks, summaries, and team knowledge. | B/I |
| 34 | Asana Intelligence | Project management AI | Teaches AI for project planning, status, risk, and team coordination. | B/I |
| 35 | Zoom AI Companion | Meeting and collaboration assistant | Common AI meeting assistant for summaries, chat, and follow-up workflows. | B/I |
| 36 | GitHub Copilot | Coding assistant | Default AI coding product for many developers and organizations. | B/I/A |
| 37 | Cursor | AI code editor | Leading AI-native IDE for codebase chat, edits, agents, and software workflows. | B/I/A |
| 38 | Windsurf | AI code editor | Popular agentic coding IDE and representative of AI-native developer environments. | B/I/A |
| 39 | Claude Code | Agentic coding tool | Fast-growing terminal coding agent with strong enterprise adoption signal. | B/I/A |
| 40 | OpenAI Codex | Coding agent | Important OpenAI coding-agent product pattern for task delegation and repository work. | B/I/A |
| 41 | Replit Agent | App builder/coding agent | Popular browser-based build environment for learners and rapid prototypes. | B/I/A |
| 42 | Bolt.new | App builder | High-usage prompt-to-app builder for web apps and prototypes. | B/I |
| 43 | Lovable | App builder | Popular text-to-app product for no-code and low-code AI product creation. | B/I |
| 44 | v0 by Vercel | UI/app generator | Important frontend generation product tied to React and Vercel workflows. | B/I |
| 45 | Devin | Autonomous software engineering agent | Representative of autonomous coding-agent workflows and review practices. | B/I/A |
| 46 | Sourcegraph Cody | Codebase assistant | Enterprise code search, understanding, and codebase chat. | B/I |
| 47 | Amazon Q Developer | Coding and cloud assistant | Major AWS coding and cloud development AI product. | B/I/A |
| 48 | JetBrains AI Assistant | IDE assistant | Important for IntelliJ, PyCharm, WebStorm, and JetBrains-heavy teams. | B/I |
| 49 | Tabnine | Coding assistant | Long-running enterprise coding assistant with privacy and deployment options. | B/I |
| 50 | Qodo | Code quality assistant | Test generation, code review, and quality-focused AI workflow. | B/I |
| 51 | CodeRabbit | AI code review | Common pull-request review assistant for engineering teams. | B/I |
| 52 | Continue | Open-source coding assistant | Teaches local/open model coding workflows inside IDEs. | B/I/A |
| 53 | Aider | Terminal coding assistant | Important command-line pair-programming workflow for Git-based changes. | B/I/A |
| 54 | Blackbox AI | Coding assistant | Popular developer assistant for code search, generation, and chat. | B/I |
| 55 | Pieces | Developer memory assistant | Teaches personal code snippets, context, and developer knowledge management. | B/I |
| 56 | Augment Code | Codebase assistant | Enterprise codebase understanding and agentic development workflow. | B/I/A |
| 57 | Zed AI | AI-native code editor | Important modern editor with integrated assistant workflows. | B/I |
| 58 | Codeium Enterprise | Coding assistant | Enterprise coding assistant lineage and deployment model. | B/I |
| 59 | CodiumAI Cover-Agent | Test generation tool | Useful for teaching AI-assisted test generation and quality gates. | B/I |
| 60 | Mutable.ai | Code intelligence tool | Documentation, codebase understanding, and engineering knowledge workflows. | B/I |
| 61 | GitHub | Developer collaboration platform | Essential platform for repositories, issues, pull requests, Actions, releases, security alerts, and AI-assisted software teamwork. | B/I/A |
| 62 | NotebookLM | Research and study assistant | Widely used document-grounded learning and briefing product. | B/I/A |
| 63 | Elicit | Research assistant | Literature review, paper discovery, and evidence extraction workflow. | B/I |
| 64 | Consensus | Research answer engine | Scientific consensus search and citation-backed answer workflow. | B/I |
| 65 | Scite | Research citation assistant | Citation context, smart citations, and evidence evaluation. | B/I |
| 66 | Semantic Scholar | Scholarly search | AI-assisted academic discovery and paper recommendation. | B/I |
| 67 | ResearchRabbit | Research discovery | Visual paper discovery, author networks, and literature mapping. | B/I |
| 68 | Connected Papers | Research graph tool | Teaches citation graph exploration and literature navigation. | B/I |
| 69 | Glean | Enterprise search and knowledge assistant | Major workplace search and knowledge assistant across enterprise sources. | B/I/A |
| 70 | Hebbia | Enterprise knowledge/research platform | High-value enterprise document analysis and financial/legal research workflows. | B/I/A |
| 71 | Sana | Enterprise knowledge and learning platform | Knowledge assistant, internal learning, and enterprise AI search. | B/I |
| 72 | Guru | Knowledge management AI | Team knowledge base with AI answers and verification workflows. | B/I |
| 73 | Coveo | AI enterprise search | Search relevance, recommendations, and support/content retrieval. | B/I |
| 74 | Algolia NeuralSearch | Search/RAG product | Teaches semantic search in ecommerce and product discovery. | B/I |
| 75 | Elastic AI Search | Search/RAG product | Enterprise search, vector search, hybrid retrieval, and observability-adjacent use. | B/I/A |
| 76 | Pinecone Assistant | RAG application layer | Teaches managed retrieval, file grounding, and assistant construction. | B/I |
| 77 | Vectara | RAG platform | Retrieval-augmented generation, grounded answers, and hallucination controls. | B/I/A |
| 78 | Onyx | Open-source workplace search | Open-source enterprise search and RAG for internal tools. | B/I/A |
| 79 | Kagi Assistant | AI search assistant | Paid search plus assistant workflow for research and synthesis. | B/I |
| 80 | Exa | Web search API | Neural web search for AI agents and retrieval products. | B/I/A |
| 81 | LlamaIndex | RAG framework | Core framework for connecting data, indexes, retrieval, and agents. | B/I/A |
| 82 | LangChain | AI app framework | Major framework for chains, tools, agents, memory, and RAG patterns. | B/I/A |
| 83 | Pinecone | Vector database | Major managed vector database for production RAG. | B/I/A |
| 84 | Weaviate | Vector database | Popular open-source and managed vector database with hybrid search. | B/I/A |
| 85 | Milvus | Vector database | Major open-source vector database, often used at scale. | B/I/A |
| 86 | Zilliz Cloud | Managed vector database | Commercial managed Milvus ecosystem. | B/I/A |
| 87 | Qdrant | Vector database | Developer-friendly vector database for semantic search and RAG. | B/I/A |
| 88 | Chroma | Vector database | Common local and prototyping vector store for RAG learners. | B/I |
| 89 | pgvector | Postgres vector extension | Practical default for teams already using PostgreSQL. | B/I/A |
| 90 | Redis Vector Search | Vector search database | Common cache plus vector search option in production stacks. | B/I |
| 91 | Elasticsearch Vector Search | Search/vector platform | Hybrid search, dense vectors, and enterprise search workloads. | B/I/A |
| 92 | OpenSearch Vector Engine | Search/vector platform | Open-source search plus vector capabilities, often AWS-aligned. | B/I/A |
| 93 | MongoDB Atlas Vector Search | Document database vector search | Common for app teams using MongoDB and RAG over JSON documents. | B/I/A |
| 94 | Azure AI Search | Search/RAG platform | Enterprise search and RAG backbone for Microsoft cloud deployments. | B/I/A |
| 95 | Vertex AI Vector Search | Vector search platform | Google Cloud vector search for production AI applications. | B/I/A |
| 96 | Amazon Bedrock Knowledge Bases | Managed RAG platform | AWS-native RAG pipeline and retrieval orchestration. | B/I/A |
| 97 | Snowflake Cortex Search | Enterprise search/RAG | Search and retrieval over enterprise data in Snowflake. | B/I/A |
| 98 | Databricks Vector Search | Lakehouse vector search | Retrieval over lakehouse data and ML workflows. | B/I/A |
| 99 | Neo4j Vector Index | Graph/vector retrieval | GraphRAG and hybrid relationship-aware retrieval. | B/I/A |
| 100 | DataStax Astra DB | Vector database | Cassandra-backed vector search and RAG app backend. | B/I |
| 101 | SingleStore Kai | Vector/data platform | Fast SQL, vector search, and transactions for AI apps. | B/I |
| 102 | LanceDB | Vector database | Embedding and multimodal vector storage using Lance format. | B/I/A |
| 103 | FAISS | Vector search library | Foundational local vector indexing library for search education. | B/I/A |
| 104 | Vespa | Search and recommendation engine | Large-scale vector, text, recommendation, and ranking engine. | B/I/A |
| 105 | Turbopuffer | Vector search service | High-scale vector search infrastructure for AI applications. | B/I/A |
| 106 | Supabase Vector | Postgres vector platform | Accessible vector/RAG workflow for web app builders. | B/I |
| 107 | Marqo | Vector search engine | Multimodal search and recommendation engine. | B/I |
| 108 | ChatGPT Advanced Data Analysis | Data analysis assistant | Common spreadsheet, charting, Python, and statistical analysis workflow. | B/I/A |
| 109 | Claude data analysis | Data analysis assistant | Strong document, spreadsheet, and artifact-based analysis workflows. | B/I/A |
| 110 | Gemini in BigQuery | Data warehouse AI | Google data analytics assistant and SQL/data workflow. | B/I/A |
| 111 | Microsoft Copilot in Power BI | BI assistant | Natural language BI, dashboard generation, and data explanation. | B/I/A |
| 112 | Tableau Pulse | BI assistant | Business metric summaries, insight surfacing, and analytics workflows. | B/I |
| 113 | ThoughtSpot Spotter | BI assistant | Search-driven analytics and natural language data exploration. | B/I |
| 114 | Looker with Gemini | BI assistant | Google Cloud BI AI workflows and semantic model querying. | B/I |
| 115 | Databricks Assistant | Data/AI engineering assistant | SQL, notebooks, lakehouse engineering, and analytics support. | B/I/A |
| 116 | Snowflake Cortex Analyst | Data assistant | Natural language analytics over governed enterprise data. | B/I/A |
| 117 | Hex Magic | Data notebook assistant | Collaborative analytics notebooks with AI code, SQL, and charting. | B/I |
| 118 | Mode AI | Analytics assistant | BI and SQL analytics assistant for business teams. | B/I |
| 119 | Julius AI | Data analysis assistant | Popular consumer/professional data analysis tool for files and charts. | B/I |
| 120 | Akkio | No-code analytics/ML | Predictive analytics and business data workflows for nontechnical users. | B/I |
| 121 | Obviously AI | No-code ML | Predictive analytics and no-code model building for business users. | B/I |
| 122 | DataRobot | Enterprise AI/ML platform | Mature enterprise AutoML, predictive AI, and governance. | B/I/A |
| 123 | H2O.ai | AI/ML platform | Open and enterprise ML, AutoML, and predictive modeling. | B/I/A |
| 124 | Dataiku | Enterprise AI platform | Enterprise analytics, ML, GenAI apps, and governed workflows. | B/I/A |
| 125 | Alteryx AiDIN | Analytics automation | Analytics automation, data prep, and AI-assisted workflows. | B/I |
| 126 | KNIME AI | Analytics workflow platform | Visual analytics, data science workflows, and AI extensions. | B/I |
| 127 | Canva Magic Studio | Design platform | Mass-market AI design, presentation, image, and marketing workflow. | B/I/A |
| 128 | Adobe Firefly | Creative generation platform | Major commercial creative AI family across Adobe products. | B/I/A |
| 129 | Photoshop Generative Fill | Image editing AI | Mainstream professional image editing workflow with generative AI. | B/I |
| 130 | Illustrator generative AI | Vector/design AI | Important for vector design, brand work, and commercial illustration. | B/I |
| 131 | Midjourney | Image generation | Defining image generation product with strong creative community usage. | B/I/A |
| 132 | ChatGPT Images | Image generation | Mainstream image generation inside the largest assistant workflow. | B/I |
| 133 | DreamStudio | Image generation | Stability AI product for Stable Diffusion workflows. | B/I |
| 134 | Leonardo AI | Image/design generation | Popular creative generation product integrated into Canva ecosystem. | B/I |
| 135 | Ideogram | Image/text generation | Strong for image generation with typography and design layouts. | B/I |
| 136 | Freepik AI | Design asset generation | Widely used stock/design asset platform with AI generation. | B/I |
| 137 | Krea | Real-time creative generation | Image generation, enhancement, and real-time creative workflows. | B/I |
| 138 | Recraft | Brand/design generation | Vector, icon, illustration, and brand-oriented generation. | B/I |
| 139 | Photoroom | Product photo editing | Popular ecommerce and marketplace image editing workflow. | B/I |
| 140 | remove.bg | Background removal | Common AI image utility used by non-designers and ecommerce teams. | B |
| 141 | Picsart AI | Consumer design/editing | Large consumer creative editing platform with AI tools. | B/I |
| 142 | Clipdrop | Image editing utilities | Useful suite for cleanup, relight, upscale, and generative fill. | B |
| 143 | Magnific | Image upscaling/enhancement | Known creative upscaling and enhancement workflow. | B/I |
| 144 | Topaz Photo AI | Photo enhancement | Professional photo denoise, sharpen, and upscale workflow. | B/I |
| 145 | Microsoft Designer | Design generation | Mainstream design generator connected to Microsoft accounts and Copilot. | B |
| 146 | Gamma | Presentation generation | Popular AI presentation and web doc generation product. | B/I |
| 147 | Runway | Video generation/editing | Leading AI video creation and editing product. | B/I/A |
| 148 | Sora | Video generation | Important OpenAI video generation product and cultural reference point. | B/I |
| 149 | Pika | Video generation | Popular consumer/prosumer AI video generation tool. | B/I |
| 150 | Luma Dream Machine | Video generation | Important AI video and 3D-adjacent generation product. | B/I |
| 151 | Kling | Video generation | High-profile AI video product with global adoption signal. | B/I |
| 152 | Hailuo AI | Video generation | MiniMax video generation product with strong consumer interest. | B/I |
| 153 | Google Veo | Video generation | Major Google video generation model/product line. | B/I |
| 154 | Synthesia | AI video avatars | Enterprise training, enablement, and avatar video generation. | B/I |
| 155 | HeyGen | AI video avatars | Popular avatar, translation, and marketing video product. | B/I |
| 156 | Descript | Audio/video editing | Transcript-first editing, overdub, clips, and podcast/video workflow. | B/I/A |
| 157 | CapCut | Video editing | Mass-market video editing product with AI-assisted creation. | B/I |
| 158 | OpusClip | Short-form video repurposing | Popular AI clipping and social video workflow. | B/I |
| 159 | ElevenLabs | Voice generation | Leading voice synthesis, dubbing, and audio generation platform. | B/I/A |
| 160 | Suno | Music generation | Popular consumer AI music generation product. | B/I |
| 161 | Udio | Music generation | Popular AI music generation product and rights discussion case. | B/I |
| 162 | Murf | Voice generation | Voiceover generation for business, training, and content. | B/I |
| 163 | Speechify | Text-to-speech | High-usage reading, accessibility, and voice product. | B/I |
| 164 | Otter.ai | Meeting transcription | Common meeting transcription and summary product. | B/I |
| 165 | Fireflies.ai | Meeting assistant | Popular meeting notes, summaries, and CRM follow-up workflow. | B/I |
| 166 | Fathom | Meeting assistant | Meeting recording, summary, and action item workflow. | B/I |
| 167 | HubSpot AI | CRM/marketing/sales AI | Common SMB CRM with AI content, sales, and support features. | B/I/A |
| 168 | Salesforce Einstein | CRM AI | Enterprise CRM AI for sales, service, marketing, and analytics. | B/I/A |
| 169 | Gong | Revenue intelligence | AI call analysis, coaching, pipeline, and revenue workflows. | B/I |
| 170 | Clari | Revenue forecasting | Pipeline inspection, forecasting, and revenue operations AI. | B/I |
| 171 | Apollo AI | Sales prospecting | Prospecting, enrichment, sequences, and sales automation. | B/I |
| 172 | Outreach Kaia | Sales engagement AI | Sales call assistant and sales workflow automation. | B/I |
| 173 | Salesloft Rhythm | Sales engagement AI | Sales engagement, prioritization, and forecasting AI. | B/I |
| 174 | 6sense Revenue AI | Account-based marketing AI | Intent data, predictive account selection, and ABM workflows. | B/I |
| 175 | Demandbase One | Account-based marketing AI | Enterprise ABM, intent, personalization, and advertising. | B/I |
| 176 | Drift | Conversational marketing | AI chat, qualification, and buyer engagement workflows. | B/I |
| 177 | Intercom Fin | Customer support AI | Widely used support chatbot and help-center answer product. | B/I |
| 178 | Zendesk AI | Customer support AI | Major support platform with AI triage, agent assist, and bots. | B/I/A |
| 179 | Freshdesk Freddy AI | Customer support AI | SMB and midmarket support AI for tickets and answers. | B/I |
| 180 | Ada | Customer support automation | AI customer service automation and bot workflows. | B/I |
| 181 | Forethought | Customer support AI | Support automation, triage, and knowledge retrieval. | B/I |
| 182 | Sierra | Customer service agent | High-profile AI customer service agent platform. | B/I |
| 183 | ServiceNow Now Assist | Enterprise service AI | ITSM, HR, customer service, and workflow AI. | B/I/A |
| 184 | Genesys Cloud AI | Contact center AI | Contact center routing, agent assist, and customer experience AI. | B/I |
| 185 | NICE Enlighten | Contact center AI | Enterprise contact center analytics and agent assist. | B/I |
| 186 | Mailchimp AI | Marketing automation AI | Email marketing, content, segmentation, and campaign support. | B/I |
| 187 | Klaviyo AI | Ecommerce marketing AI | Ecommerce email/SMS personalization and predictive marketing. | B/I |
| 188 | Hootsuite OwlyWriter AI | Social media AI | Social content generation and management workflow. | B |
| 189 | Semrush ContentShake AI | SEO/content AI | SEO content planning and drafting workflow. | B/I |
| 190 | Surfer SEO | SEO content AI | Search-optimized content planning and writing. | B/I |
| 191 | Clay | GTM data automation | Enrichment, prospecting, and AI research workflows for sales teams. | B/I/A |
| 192 | Zapier AI | Workflow automation AI | Mainstream no-code automation with AI actions and agents. | B/I/A |
| 193 | Make AI | Workflow automation AI | Visual automation and integration workflows with AI modules. | B/I |
| 194 | n8n | Workflow automation | Open-source automation and agent workflows. | B/I/A |
| 195 | Microsoft Copilot Studio | Agent/workflow builder | Enterprise agent creation and Microsoft ecosystem automation. | B/I/A |
| 196 | Google Agentspace | Enterprise agent/search platform | Google enterprise agents, search, and workplace AI direction. | B/I |
| 197 | Salesforce Agentforce | Enterprise agent platform | CRM-native agents for sales, service, marketing, and commerce. | B/I/A |
| 198 | UiPath Autopilot | RPA/automation AI | AI-assisted robotic process automation and workflow mining. | B/I/A |
| 199 | Automation Anywhere | RPA/automation AI | Enterprise process automation and AI agent workflows. | B/I |
| 200 | Workato | Integration automation AI | Enterprise integration, workflow automation, and AI actions. | B/I |
| 201 | Lindy | Personal/team AI agents | Popular agent builder for administrative and sales workflows. | B/I |
| 202 | Relevance AI | Agent builder | No-code/low-code agent teams and workflow automation. | B/I |
| 203 | CrewAI | Agent framework | Multi-agent orchestration framework for developer workflows. | B/I/A |
| 204 | LangGraph | Agent framework | Graph-based agent orchestration for production AI workflows. | B/I/A |
| 205 | Dust | Enterprise AI assistants | Internal assistants, knowledge integrations, and custom workflows. | B/I |
| 206 | Gumloop | Workflow automation AI | Visual AI automation for teams and operations. | B/I |
| 207 | Manus | General agent | Consumer/general autonomous task agent and agentic UX example. | B/I |
| 208 | Airtable AI | Work app/database AI | AI inside lightweight databases and operational apps. | B/I |
| 209 | Retool AI | Internal tools AI | AI features and agents for internal business software. | B/I/A |
| 210 | Voiceflow | Conversational agent builder | Chatbot and voice assistant design/build platform. | B/I |
| 211 | OpenAI API | Model/API platform | Core model API ecosystem for chat, agents, vision, audio, and embeddings. | B/I/A |
| 212 | Anthropic Claude API | Model/API platform | Major enterprise model API, long context, tool use, and coding workflows. | B/I/A |
| 213 | Google Vertex AI | Cloud AI platform | Google model hosting, Gemini APIs, agents, tuning, and MLOps. | B/I/A |
| 214 | Azure AI Foundry | Cloud AI platform | Microsoft enterprise AI app, model, agent, and governance platform. | B/I/A |
| 215 | Amazon Bedrock | Cloud AI platform | AWS managed model marketplace, agents, knowledge bases, and guardrails. | B/I/A |
| 216 | Cohere | Model/API platform | Enterprise LLMs, embeddings, reranking, and retrieval workflows. | B/I/A |
| 217 | Mistral AI API | Model/API platform | European model provider with open and commercial model offerings. | B/I/A |
| 218 | xAI API | Model/API platform | Grok model access and X-adjacent AI ecosystem. | B/I |
| 219 | DeepSeek API | Model/API platform | Low-cost reasoning/coding model ecosystem and open-model comparison. | B/I |
| 220 | Together AI | Model hosting/API platform | Open model inference, fine-tuning, and deployment platform. | B/I/A |
| 221 | Fireworks AI | Model serving/API platform | Fast inference and deployment for open models. | B/I/A |
| 222 | GroqCloud | Inference platform | High-speed inference platform and model API. | B/I |
| 223 | Hugging Face | Model hub/platform | Central open model, dataset, Spaces, and inference ecosystem. | B/I/A |
| 224 | Replicate | Model API platform | Hosted open-source model APIs and creative/model experimentation. | B/I |
| 225 | OpenRouter | Model routing API | Multi-model routing, comparison, and application fallback strategy. | B/I/A |
| 226 | Cerebras Inference | Inference platform | High-speed inference API and hardware-backed model serving. | B/I |
| 227 | Databricks Mosaic AI | Enterprise AI platform | Model serving, training, governance, and lakehouse AI. | B/I/A |
| 228 | IBM watsonx | Enterprise AI platform | Enterprise AI, governance, model deployment, and regulated workflows. | B/I/A |
| 229 | NVIDIA NIM | Model deployment platform | Enterprise model deployment and GPU-optimized inference microservices. | B/I/A |
| 230 | AI21 Labs | Model/API platform | Enterprise language models and writing/reading APIs. | B/I |
| 231 | Harvey | Legal AI | Leading legal AI assistant for law firms and legal teams. | B/I/A |
| 232 | CoCounsel | Legal AI | Legal research, document review, and professional legal workflow. | B/I/A |
| 233 | Lexis+ AI | Legal research AI | Mainstream legal research and drafting AI in LexisNexis ecosystem. | B/I/A |
| 234 | Westlaw Precision AI | Legal research AI | Thomson Reuters legal research and drafting AI workflow. | B/I/A |
| 235 | Ironclad AI | Contract lifecycle AI | Contract review, clause analysis, and legal operations. | B/I |
| 236 | Abridge | Healthcare documentation AI | Clinical note generation and ambient medical documentation. | B/I/A |
| 237 | Nabla | Healthcare documentation AI | Ambient clinical assistant and note automation. | B/I |
| 238 | Nuance DAX Copilot | Healthcare documentation AI | Microsoft/Nuance ambient clinical documentation product. | B/I/A |
| 239 | Ambience Healthcare | Healthcare documentation AI | Clinical AI operating system and documentation workflows. | B/I |
| 240 | Suki | Healthcare assistant | Physician documentation and workflow assistant. | B/I |
| 241 | AlphaSense | Market intelligence AI | Enterprise research, earnings, filings, and market intelligence. | B/I/A |
| 242 | Bloomberg Terminal AI | Finance AI | Financial research, news, and market intelligence AI workflows. | B/I/A |
| 243 | Ramp Intelligence | Finance operations AI | Spend management, policy automation, procurement, and finance operations AI. | B/I |
| 244 | Brex AI | Finance operations AI | Corporate card, expense, travel, and spend management AI. | B/I |
| 245 | Microsoft Security Copilot | Security AI | Enterprise security investigation, summarization, and response. | B/I/A |
| 246 | CrowdStrike Charlotte AI | Security AI | Security operations and endpoint threat investigation assistant. | B/I/A |
| 247 | SentinelOne Purple AI | Security AI | Security analysis, hunting, and SOC assistance. | B/I/A |
| 248 | Darktrace | Cybersecurity AI | Network detection, response, and security analytics AI. | B/I |
| 249 | Vectra AI | Cybersecurity AI | Network detection and response using AI-driven threat analysis. | B/I |
| 250 | Snyk AI | Developer security AI | AI-assisted code security, dependency, and vulnerability workflows. | B/I |

## Expansion Tracks

Rows 251-500 extend the Products Ladder into workforce, operations, industry, scientific, and personal-productivity software. These are implemented as first-class product cards rather than a separate request queue.

| 251 | Eightfold AI | HR, recruiting, and talent intelligence | Adds Eightfold AI to the workforce AI track for sourcing, screening, candidate experience, talent intelligence, and hiring-risk literacy. | B/I |
| 252 | SeekOut | HR, recruiting, and talent intelligence | Adds SeekOut to the workforce AI track for sourcing, screening, candidate experience, talent intelligence, and hiring-risk literacy. | B/I |
| 253 | HireVue | HR, recruiting, and talent intelligence | Adds HireVue to the workforce AI track for sourcing, screening, candidate experience, talent intelligence, and hiring-risk literacy. | B/I |
| 254 | Paradox | HR, recruiting, and talent intelligence | Adds Paradox to the workforce AI track for sourcing, screening, candidate experience, talent intelligence, and hiring-risk literacy. | B/I |
| 255 | Phenom | HR, recruiting, and talent intelligence | Adds Phenom to the workforce AI track for sourcing, screening, candidate experience, talent intelligence, and hiring-risk literacy. | B/I |
| 256 | Beamery | HR, recruiting, and talent intelligence | Adds Beamery to the workforce AI track for sourcing, screening, candidate experience, talent intelligence, and hiring-risk literacy. | B/I |
| 257 | hireEZ | HR, recruiting, and talent intelligence | Adds hireEZ to the workforce AI track for sourcing, screening, candidate experience, talent intelligence, and hiring-risk literacy. | B/I |
| 258 | Fetcher | HR, recruiting, and talent intelligence | Adds Fetcher to the workforce AI track for sourcing, screening, candidate experience, talent intelligence, and hiring-risk literacy. | B/I |
| 259 | Loxo | HR, recruiting, and talent intelligence | Adds Loxo to the workforce AI track for sourcing, screening, candidate experience, talent intelligence, and hiring-risk literacy. | B/I |
| 260 | Manatal | HR, recruiting, and talent intelligence | Adds Manatal to the workforce AI track for sourcing, screening, candidate experience, talent intelligence, and hiring-risk literacy. | B/I |
| 261 | Greenhouse AI | HR, recruiting, and talent intelligence | Adds Greenhouse AI to the workforce AI track for sourcing, screening, candidate experience, talent intelligence, and hiring-risk literacy. | B/I |
| 262 | Lever AI | HR, recruiting, and talent intelligence | Adds Lever AI to the workforce AI track for sourcing, screening, candidate experience, talent intelligence, and hiring-risk literacy. | B/I |
| 263 | Workable AI | HR, recruiting, and talent intelligence | Adds Workable AI to the workforce AI track for sourcing, screening, candidate experience, talent intelligence, and hiring-risk literacy. | B/I |
| 264 | Ashby | HR, recruiting, and talent intelligence | Adds Ashby to the workforce AI track for sourcing, screening, candidate experience, talent intelligence, and hiring-risk literacy. | B/I |
| 265 | Gem | HR, recruiting, and talent intelligence | Adds Gem to the workforce AI track for sourcing, screening, candidate experience, talent intelligence, and hiring-risk literacy. | B/I |
| 266 | Humanly | HR, recruiting, and talent intelligence | Adds Humanly to the workforce AI track for sourcing, screening, candidate experience, talent intelligence, and hiring-risk literacy. | B/I |
| 267 | XOR | HR, recruiting, and talent intelligence | Adds XOR to the workforce AI track for sourcing, screening, candidate experience, talent intelligence, and hiring-risk literacy. | B/I |
| 268 | iCIMS Copilot | HR, recruiting, and talent intelligence | Adds iCIMS Copilot to the workforce AI track for sourcing, screening, candidate experience, talent intelligence, and hiring-risk literacy. | B/I |
| 269 | SmartRecruiters Winston | HR, recruiting, and talent intelligence | Adds SmartRecruiters Winston to the workforce AI track for sourcing, screening, candidate experience, talent intelligence, and hiring-risk literacy. | B/I |
| 270 | Textio | HR, recruiting, and talent intelligence | Adds Textio to the workforce AI track for sourcing, screening, candidate experience, talent intelligence, and hiring-risk literacy. | B/I |
| 271 | Pymetrics | HR, recruiting, and talent intelligence | Adds Pymetrics to the workforce AI track for sourcing, screening, candidate experience, talent intelligence, and hiring-risk literacy. | B/I |
| 272 | Workday HiredScore | HR, recruiting, and talent intelligence | Adds Workday HiredScore to the workforce AI track for sourcing, screening, candidate experience, talent intelligence, and hiring-risk literacy. | B/I |
| 273 | SAP SuccessFactors AI | HR, recruiting, and talent intelligence | Adds SAP SuccessFactors AI to the workforce AI track for sourcing, screening, candidate experience, talent intelligence, and hiring-risk literacy. | B/I |
| 274 | Oracle Recruiting AI | HR, recruiting, and talent intelligence | Adds Oracle Recruiting AI to the workforce AI track for sourcing, screening, candidate experience, talent intelligence, and hiring-risk literacy. | B/I |
| 275 | LinkedIn Recruiter AI | HR, recruiting, and talent intelligence | Adds LinkedIn Recruiter AI to the workforce AI track for sourcing, screening, candidate experience, talent intelligence, and hiring-risk literacy. | B/I |
| 276 | Khanmigo | Education, tutoring, and classroom AI | Adds Khanmigo to the education AI track for tutoring, teacher workflow, differentiation, grading, standards alignment, and academic integrity. | B/I |
| 277 | MagicSchool AI | Education, tutoring, and classroom AI | Adds MagicSchool AI to the education AI track for tutoring, teacher workflow, differentiation, grading, standards alignment, and academic integrity. | B/I |
| 278 | Brisk Teaching | Education, tutoring, and classroom AI | Adds Brisk Teaching to the education AI track for tutoring, teacher workflow, differentiation, grading, standards alignment, and academic integrity. | B/I |
| 279 | Diffit | Education, tutoring, and classroom AI | Adds Diffit to the education AI track for tutoring, teacher workflow, differentiation, grading, standards alignment, and academic integrity. | B/I |
| 280 | Eduaide.AI | Education, tutoring, and classroom AI | Adds Eduaide.AI to the education AI track for tutoring, teacher workflow, differentiation, grading, standards alignment, and academic integrity. | B/I |
| 281 | SchoolAI | Education, tutoring, and classroom AI | Adds SchoolAI to the education AI track for tutoring, teacher workflow, differentiation, grading, standards alignment, and academic integrity. | B/I |
| 282 | Curipod | Education, tutoring, and classroom AI | Adds Curipod to the education AI track for tutoring, teacher workflow, differentiation, grading, standards alignment, and academic integrity. | B/I |
| 283 | Gradescope | Education, tutoring, and classroom AI | Adds Gradescope to the education AI track for tutoring, teacher workflow, differentiation, grading, standards alignment, and academic integrity. | B/I |
| 284 | Synthesis Tutor | Education, tutoring, and classroom AI | Adds Synthesis Tutor to the education AI track for tutoring, teacher workflow, differentiation, grading, standards alignment, and academic integrity. | B/I |
| 285 | Squirrel AI | Education, tutoring, and classroom AI | Adds Squirrel AI to the education AI track for tutoring, teacher workflow, differentiation, grading, standards alignment, and academic integrity. | B/I |
| 286 | Carnegie Learning MATHia | Education, tutoring, and classroom AI | Adds Carnegie Learning MATHia to the education AI track for tutoring, teacher workflow, differentiation, grading, standards alignment, and academic integrity. | B/I |
| 287 | Duolingo Max | Education, tutoring, and classroom AI | Adds Duolingo Max to the education AI track for tutoring, teacher workflow, differentiation, grading, standards alignment, and academic integrity. | B/I |
| 288 | Speak | Education, tutoring, and classroom AI | Adds Speak to the education AI track for tutoring, teacher workflow, differentiation, grading, standards alignment, and academic integrity. | B/I |
| 289 | Praktika | Education, tutoring, and classroom AI | Adds Praktika to the education AI track for tutoring, teacher workflow, differentiation, grading, standards alignment, and academic integrity. | B/I |
| 290 | TalkPal | Education, tutoring, and classroom AI | Adds TalkPal to the education AI track for tutoring, teacher workflow, differentiation, grading, standards alignment, and academic integrity. | B/I |
| 291 | ELSA Speak | Education, tutoring, and classroom AI | Adds ELSA Speak to the education AI track for tutoring, teacher workflow, differentiation, grading, standards alignment, and academic integrity. | B/I |
| 292 | Quizlet AI | Education, tutoring, and classroom AI | Adds Quizlet AI to the education AI track for tutoring, teacher workflow, differentiation, grading, standards alignment, and academic integrity. | B/I |
| 293 | Socratic by Google | Education, tutoring, and classroom AI | Adds Socratic by Google to the education AI track for tutoring, teacher workflow, differentiation, grading, standards alignment, and academic integrity. | B/I |
| 294 | Photomath | Education, tutoring, and classroom AI | Adds Photomath to the education AI track for tutoring, teacher workflow, differentiation, grading, standards alignment, and academic integrity. | B/I |
| 295 | Wolfram Alpha | Education, tutoring, and classroom AI | Adds Wolfram Alpha to the education AI track for tutoring, teacher workflow, differentiation, grading, standards alignment, and academic integrity. | B/I |
| 296 | Knewton Alta | Education, tutoring, and classroom AI | Adds Knewton Alta to the education AI track for tutoring, teacher workflow, differentiation, grading, standards alignment, and academic integrity. | B/I |
| 297 | CENTURY Tech | Education, tutoring, and classroom AI | Adds CENTURY Tech to the education AI track for tutoring, teacher workflow, differentiation, grading, standards alignment, and academic integrity. | B/I |
| 298 | DreamBox Math | Education, tutoring, and classroom AI | Adds DreamBox Math to the education AI track for tutoring, teacher workflow, differentiation, grading, standards alignment, and academic integrity. | B/I |
| 299 | IXL | Education, tutoring, and classroom AI | Adds IXL to the education AI track for tutoring, teacher workflow, differentiation, grading, standards alignment, and academic integrity. | B/I |
| 300 | Cognii | Education, tutoring, and classroom AI | Adds Cognii to the education AI track for tutoring, teacher workflow, differentiation, grading, standards alignment, and academic integrity. | B/I |
| 301 | Constructor | Ecommerce, retail, and merchandising AI | Adds Constructor to the commerce AI track for product discovery, recommendations, personalization, merchandising controls, and agentic shopping readiness. | B/I |
| 302 | Bloomreach Loomi | Ecommerce, retail, and merchandising AI | Adds Bloomreach Loomi to the commerce AI track for product discovery, recommendations, personalization, merchandising controls, and agentic shopping readiness. | B/I |
| 303 | Nosto | Ecommerce, retail, and merchandising AI | Adds Nosto to the commerce AI track for product discovery, recommendations, personalization, merchandising controls, and agentic shopping readiness. | B/I |
| 304 | Dynamic Yield | Ecommerce, retail, and merchandising AI | Adds Dynamic Yield to the commerce AI track for product discovery, recommendations, personalization, merchandising controls, and agentic shopping readiness. | B/I |
| 305 | Klevu | Ecommerce, retail, and merchandising AI | Adds Klevu to the commerce AI track for product discovery, recommendations, personalization, merchandising controls, and agentic shopping readiness. | B/I |
| 306 | Searchspring | Ecommerce, retail, and merchandising AI | Adds Searchspring to the commerce AI track for product discovery, recommendations, personalization, merchandising controls, and agentic shopping readiness. | B/I |
| 307 | Clerk.io | Ecommerce, retail, and merchandising AI | Adds Clerk.io to the commerce AI track for product discovery, recommendations, personalization, merchandising controls, and agentic shopping readiness. | B/I |
| 308 | Barilliance | Ecommerce, retail, and merchandising AI | Adds Barilliance to the commerce AI track for product discovery, recommendations, personalization, merchandising controls, and agentic shopping readiness. | B/I |
| 309 | Rebuy | Ecommerce, retail, and merchandising AI | Adds Rebuy to the commerce AI track for product discovery, recommendations, personalization, merchandising controls, and agentic shopping readiness. | B/I |
| 310 | LimeSpot | Ecommerce, retail, and merchandising AI | Adds LimeSpot to the commerce AI track for product discovery, recommendations, personalization, merchandising controls, and agentic shopping readiness. | B/I |
| 311 | Netcore Unbxd | Ecommerce, retail, and merchandising AI | Adds Netcore Unbxd to the commerce AI track for product discovery, recommendations, personalization, merchandising controls, and agentic shopping readiness. | B/I |
| 312 | Shaped | Ecommerce, retail, and merchandising AI | Adds Shaped to the commerce AI track for product discovery, recommendations, personalization, merchandising controls, and agentic shopping readiness. | B/I |
| 313 | Nobi | Ecommerce, retail, and merchandising AI | Adds Nobi to the commerce AI track for product discovery, recommendations, personalization, merchandising controls, and agentic shopping readiness. | B/I |
| 314 | ViSenze | Ecommerce, retail, and merchandising AI | Adds ViSenze to the commerce AI track for product discovery, recommendations, personalization, merchandising controls, and agentic shopping readiness. | B/I |
| 315 | Syte | Ecommerce, retail, and merchandising AI | Adds Syte to the commerce AI track for product discovery, recommendations, personalization, merchandising controls, and agentic shopping readiness. | B/I |
| 316 | Vue.ai | Ecommerce, retail, and merchandising AI | Adds Vue.ai to the commerce AI track for product discovery, recommendations, personalization, merchandising controls, and agentic shopping readiness. | B/I |
| 317 | Lily AI | Ecommerce, retail, and merchandising AI | Adds Lily AI to the commerce AI track for product discovery, recommendations, personalization, merchandising controls, and agentic shopping readiness. | B/I |
| 318 | Bluecore | Ecommerce, retail, and merchandising AI | Adds Bluecore to the commerce AI track for product discovery, recommendations, personalization, merchandising controls, and agentic shopping readiness. | B/I |
| 319 | Insider | Ecommerce, retail, and merchandising AI | Adds Insider to the commerce AI track for product discovery, recommendations, personalization, merchandising controls, and agentic shopping readiness. | B/I |
| 320 | Adobe Target AI | Ecommerce, retail, and merchandising AI | Adds Adobe Target AI to the commerce AI track for product discovery, recommendations, personalization, merchandising controls, and agentic shopping readiness. | B/I |
| 321 | Amazon Personalize | Ecommerce, retail, and merchandising AI | Adds Amazon Personalize to the commerce AI track for product discovery, recommendations, personalization, merchandising controls, and agentic shopping readiness. | B/I |
| 322 | Google Cloud Discovery AI | Ecommerce, retail, and merchandising AI | Adds Google Cloud Discovery AI to the commerce AI track for product discovery, recommendations, personalization, merchandising controls, and agentic shopping readiness. | B/I |
| 323 | Shopify Magic | Ecommerce, retail, and merchandising AI | Adds Shopify Magic to the commerce AI track for product discovery, recommendations, personalization, merchandising controls, and agentic shopping readiness. | B/I |
| 324 | Yotpo AI | Ecommerce, retail, and merchandising AI | Adds Yotpo AI to the commerce AI track for product discovery, recommendations, personalization, merchandising controls, and agentic shopping readiness. | B/I |
| 325 | Gorgias AI | Ecommerce, retail, and merchandising AI | Adds Gorgias AI to the commerce AI track for product discovery, recommendations, personalization, merchandising controls, and agentic shopping readiness. | B/I |
| 326 | QuickBooks Intuit Assist | Finance, accounting, FP&A, procurement, and tax AI | Adds QuickBooks Intuit Assist to the finance AI track for invoice automation, close management, forecasting, procurement, expense review, tax research, and controls. | B/I/A |
| 327 | Xero JAX | Finance, accounting, FP&A, procurement, and tax AI | Adds Xero JAX to the finance AI track for invoice automation, close management, forecasting, procurement, expense review, tax research, and controls. | B/I/A |
| 328 | Dext | Finance, accounting, FP&A, procurement, and tax AI | Adds Dext to the finance AI track for invoice automation, close management, forecasting, procurement, expense review, tax research, and controls. | B/I/A |
| 329 | Vic.ai | Finance, accounting, FP&A, procurement, and tax AI | Adds Vic.ai to the finance AI track for invoice automation, close management, forecasting, procurement, expense review, tax research, and controls. | B/I/A |
| 330 | Botkeeper | Finance, accounting, FP&A, procurement, and tax AI | Adds Botkeeper to the finance AI track for invoice automation, close management, forecasting, procurement, expense review, tax research, and controls. | B/I/A |
| 331 | BILL AI | Finance, accounting, FP&A, procurement, and tax AI | Adds BILL AI to the finance AI track for invoice automation, close management, forecasting, procurement, expense review, tax research, and controls. | B/I/A |
| 332 | Tipalti Pi | Finance, accounting, FP&A, procurement, and tax AI | Adds Tipalti Pi to the finance AI track for invoice automation, close management, forecasting, procurement, expense review, tax research, and controls. | B/I/A |
| 333 | Stampli | Finance, accounting, FP&A, procurement, and tax AI | Adds Stampli to the finance AI track for invoice automation, close management, forecasting, procurement, expense review, tax research, and controls. | B/I/A |
| 334 | HighRadius Autonomous Finance | Finance, accounting, FP&A, procurement, and tax AI | Adds HighRadius Autonomous Finance to the finance AI track for invoice automation, close management, forecasting, procurement, expense review, tax research, and controls. | B/I/A |
| 335 | BlackLine | Finance, accounting, FP&A, procurement, and tax AI | Adds BlackLine to the finance AI track for invoice automation, close management, forecasting, procurement, expense review, tax research, and controls. | B/I/A |
| 336 | Trullion | Finance, accounting, FP&A, procurement, and tax AI | Adds Trullion to the finance AI track for invoice automation, close management, forecasting, procurement, expense review, tax research, and controls. | B/I/A |
| 337 | Numeric | Finance, accounting, FP&A, procurement, and tax AI | Adds Numeric to the finance AI track for invoice automation, close management, forecasting, procurement, expense review, tax research, and controls. | B/I/A |
| 338 | Planful Predict | Finance, accounting, FP&A, procurement, and tax AI | Adds Planful Predict to the finance AI track for invoice automation, close management, forecasting, procurement, expense review, tax research, and controls. | B/I/A |
| 339 | Pigment AI | Finance, accounting, FP&A, procurement, and tax AI | Adds Pigment AI to the finance AI track for invoice automation, close management, forecasting, procurement, expense review, tax research, and controls. | B/I/A |
| 340 | Anaplan PlanIQ | Finance, accounting, FP&A, procurement, and tax AI | Adds Anaplan PlanIQ to the finance AI track for invoice automation, close management, forecasting, procurement, expense review, tax research, and controls. | B/I/A |
| 341 | Workday Adaptive Planning AI | Finance, accounting, FP&A, procurement, and tax AI | Adds Workday Adaptive Planning AI to the finance AI track for invoice automation, close management, forecasting, procurement, expense review, tax research, and controls. | B/I/A |
| 342 | Oracle Fusion Cloud ERP AI | Finance, accounting, FP&A, procurement, and tax AI | Adds Oracle Fusion Cloud ERP AI to the finance AI track for invoice automation, close management, forecasting, procurement, expense review, tax research, and controls. | B/I/A |
| 343 | SAP Joule for Finance | Finance, accounting, FP&A, procurement, and tax AI | Adds SAP Joule for Finance to the finance AI track for invoice automation, close management, forecasting, procurement, expense review, tax research, and controls. | B/I/A |
| 344 | Expensify Concierge | Finance, accounting, FP&A, procurement, and tax AI | Adds Expensify Concierge to the finance AI track for invoice automation, close management, forecasting, procurement, expense review, tax research, and controls. | B/I/A |
| 345 | Navan AI | Finance, accounting, FP&A, procurement, and tax AI | Adds Navan AI to the finance AI track for invoice automation, close management, forecasting, procurement, expense review, tax research, and controls. | B/I/A |
| 346 | Airbase AI | Finance, accounting, FP&A, procurement, and tax AI | Adds Airbase AI to the finance AI track for invoice automation, close management, forecasting, procurement, expense review, tax research, and controls. | B/I/A |
| 347 | Coupa Navi | Finance, accounting, FP&A, procurement, and tax AI | Adds Coupa Navi to the finance AI track for invoice automation, close management, forecasting, procurement, expense review, tax research, and controls. | B/I/A |
| 348 | Avalara AvaTax AI | Finance, accounting, FP&A, procurement, and tax AI | Adds Avalara AvaTax AI to the finance AI track for invoice automation, close management, forecasting, procurement, expense review, tax research, and controls. | B/I/A |
| 349 | Blue J Tax | Finance, accounting, FP&A, procurement, and tax AI | Adds Blue J Tax to the finance AI track for invoice automation, close management, forecasting, procurement, expense review, tax research, and controls. | B/I/A |
| 350 | TaxDome AI | Finance, accounting, FP&A, procurement, and tax AI | Adds TaxDome AI to the finance AI track for invoice automation, close management, forecasting, procurement, expense review, tax research, and controls. | B/I/A |
| 351 | Datadog Bits AI | AIOps, observability, and incident response | Adds Datadog Bits AI to the operations AI track for alert correlation, root-cause analysis, incident summaries, runbooks, remediation, and SRE judgment. | B/I/A |
| 352 | Dynatrace Davis AI | AIOps, observability, and incident response | Adds Dynatrace Davis AI to the operations AI track for alert correlation, root-cause analysis, incident summaries, runbooks, remediation, and SRE judgment. | B/I/A |
| 353 | New Relic AI | AIOps, observability, and incident response | Adds New Relic AI to the operations AI track for alert correlation, root-cause analysis, incident summaries, runbooks, remediation, and SRE judgment. | B/I/A |
| 354 | PagerDuty AIOps | AIOps, observability, and incident response | Adds PagerDuty AIOps to the operations AI track for alert correlation, root-cause analysis, incident summaries, runbooks, remediation, and SRE judgment. | B/I/A |
| 355 | BigPanda | AIOps, observability, and incident response | Adds BigPanda to the operations AI track for alert correlation, root-cause analysis, incident summaries, runbooks, remediation, and SRE judgment. | B/I/A |
| 356 | APEX AIOps | AIOps, observability, and incident response | Adds APEX AIOps to the operations AI track for alert correlation, root-cause analysis, incident summaries, runbooks, remediation, and SRE judgment. | B/I/A |
| 357 | Splunk ITSI | AIOps, observability, and incident response | Adds Splunk ITSI to the operations AI track for alert correlation, root-cause analysis, incident summaries, runbooks, remediation, and SRE judgment. | B/I/A |
| 358 | LogicMonitor Edwin AI | AIOps, observability, and incident response | Adds LogicMonitor Edwin AI to the operations AI track for alert correlation, root-cause analysis, incident summaries, runbooks, remediation, and SRE judgment. | B/I/A |
| 359 | ScienceLogic SL1 | AIOps, observability, and incident response | Adds ScienceLogic SL1 to the operations AI track for alert correlation, root-cause analysis, incident summaries, runbooks, remediation, and SRE judgment. | B/I/A |
| 360 | IBM Instana AI | AIOps, observability, and incident response | Adds IBM Instana AI to the operations AI track for alert correlation, root-cause analysis, incident summaries, runbooks, remediation, and SRE judgment. | B/I/A |
| 361 | Cisco ThousandEyes | AIOps, observability, and incident response | Adds Cisco ThousandEyes to the operations AI track for alert correlation, root-cause analysis, incident summaries, runbooks, remediation, and SRE judgment. | B/I/A |
| 362 | Grafana Assistant | AIOps, observability, and incident response | Adds Grafana Assistant to the operations AI track for alert correlation, root-cause analysis, incident summaries, runbooks, remediation, and SRE judgment. | B/I/A |
| 363 | Chronosphere | AIOps, observability, and incident response | Adds Chronosphere to the operations AI track for alert correlation, root-cause analysis, incident summaries, runbooks, remediation, and SRE judgment. | B/I/A |
| 364 | Honeycomb Query Assistant | AIOps, observability, and incident response | Adds Honeycomb Query Assistant to the operations AI track for alert correlation, root-cause analysis, incident summaries, runbooks, remediation, and SRE judgment. | B/I/A |
| 365 | Sumo Logic Mo Copilot | AIOps, observability, and incident response | Adds Sumo Logic Mo Copilot to the operations AI track for alert correlation, root-cause analysis, incident summaries, runbooks, remediation, and SRE judgment. | B/I/A |
| 366 | Elastic Observability AI Assistant | AIOps, observability, and incident response | Adds Elastic Observability AI Assistant to the operations AI track for alert correlation, root-cause analysis, incident summaries, runbooks, remediation, and SRE judgment. | B/I/A |
| 367 | AWS DevOps Guru | AIOps, observability, and incident response | Adds AWS DevOps Guru to the operations AI track for alert correlation, root-cause analysis, incident summaries, runbooks, remediation, and SRE judgment. | B/I/A |
| 368 | Google Cloud Gemini Cloud Assist | AIOps, observability, and incident response | Adds Google Cloud Gemini Cloud Assist to the operations AI track for alert correlation, root-cause analysis, incident summaries, runbooks, remediation, and SRE judgment. | B/I/A |
| 369 | Azure Monitor Copilot | AIOps, observability, and incident response | Adds Azure Monitor Copilot to the operations AI track for alert correlation, root-cause analysis, incident summaries, runbooks, remediation, and SRE judgment. | B/I/A |
| 370 | incident.io AI | AIOps, observability, and incident response | Adds incident.io AI to the operations AI track for alert correlation, root-cause analysis, incident summaries, runbooks, remediation, and SRE judgment. | B/I/A |
| 371 | Rootly AI | AIOps, observability, and incident response | Adds Rootly AI to the operations AI track for alert correlation, root-cause analysis, incident summaries, runbooks, remediation, and SRE judgment. | B/I/A |
| 372 | OpsLevel AI | AIOps, observability, and incident response | Adds OpsLevel AI to the operations AI track for alert correlation, root-cause analysis, incident summaries, runbooks, remediation, and SRE judgment. | B/I/A |
| 373 | Kubiya | AIOps, observability, and incident response | Adds Kubiya to the operations AI track for alert correlation, root-cause analysis, incident summaries, runbooks, remediation, and SRE judgment. | B/I/A |
| 374 | Harness AI | AIOps, observability, and incident response | Adds Harness AI to the operations AI track for alert correlation, root-cause analysis, incident summaries, runbooks, remediation, and SRE judgment. | B/I/A |
| 375 | Atlassian Compass AI | AIOps, observability, and incident response | Adds Atlassian Compass AI to the operations AI track for alert correlation, root-cause analysis, incident summaries, runbooks, remediation, and SRE judgment. | B/I/A |
| 376 | Credo AI | AI governance, model risk, privacy, and compliance | Adds Credo AI to the AI governance track for inventories, policy controls, model risk, leakage prevention, compliance mapping, and audit evidence. | B/I/A |
| 377 | Holistic AI | AI governance, model risk, privacy, and compliance | Adds Holistic AI to the AI governance track for inventories, policy controls, model risk, leakage prevention, compliance mapping, and audit evidence. | B/I/A |
| 378 | Fairly AI | AI governance, model risk, privacy, and compliance | Adds Fairly AI to the AI governance track for inventories, policy controls, model risk, leakage prevention, compliance mapping, and audit evidence. | B/I/A |
| 379 | Modulos | AI governance, model risk, privacy, and compliance | Adds Modulos to the AI governance track for inventories, policy controls, model risk, leakage prevention, compliance mapping, and audit evidence. | B/I/A |
| 380 | Monitaur | AI governance, model risk, privacy, and compliance | Adds Monitaur to the AI governance track for inventories, policy controls, model risk, leakage prevention, compliance mapping, and audit evidence. | B/I/A |
| 381 | ModelOp Center | AI governance, model risk, privacy, and compliance | Adds ModelOp Center to the AI governance track for inventories, policy controls, model risk, leakage prevention, compliance mapping, and audit evidence. | B/I/A |
| 382 | OneTrust AI Governance | AI governance, model risk, privacy, and compliance | Adds OneTrust AI Governance to the AI governance track for inventories, policy controls, model risk, leakage prevention, compliance mapping, and audit evidence. | B/I/A |
| 383 | Diligent AI Risk Essentials | AI governance, model risk, privacy, and compliance | Adds Diligent AI Risk Essentials to the AI governance track for inventories, policy controls, model risk, leakage prevention, compliance mapping, and audit evidence. | B/I/A |
| 384 | Microsoft Purview AI Hub | AI governance, model risk, privacy, and compliance | Adds Microsoft Purview AI Hub to the AI governance track for inventories, policy controls, model risk, leakage prevention, compliance mapping, and audit evidence. | B/I/A |
| 385 | Google Model Armor | AI governance, model risk, privacy, and compliance | Adds Google Model Armor to the AI governance track for inventories, policy controls, model risk, leakage prevention, compliance mapping, and audit evidence. | B/I/A |
| 386 | Lakera Guard | AI governance, model risk, privacy, and compliance | Adds Lakera Guard to the AI governance track for inventories, policy controls, model risk, leakage prevention, compliance mapping, and audit evidence. | B/I/A |
| 387 | CalypsoAI | AI governance, model risk, privacy, and compliance | Adds CalypsoAI to the AI governance track for inventories, policy controls, model risk, leakage prevention, compliance mapping, and audit evidence. | B/I/A |
| 388 | Protect AI | AI governance, model risk, privacy, and compliance | Adds Protect AI to the AI governance track for inventories, policy controls, model risk, leakage prevention, compliance mapping, and audit evidence. | B/I/A |
| 389 | HiddenLayer | AI governance, model risk, privacy, and compliance | Adds HiddenLayer to the AI governance track for inventories, policy controls, model risk, leakage prevention, compliance mapping, and audit evidence. | B/I/A |
| 390 | BigID | AI governance, model risk, privacy, and compliance | Adds BigID to the AI governance track for inventories, policy controls, model risk, leakage prevention, compliance mapping, and audit evidence. | B/I/A |
| 391 | Nightfall AI | AI governance, model risk, privacy, and compliance | Adds Nightfall AI to the AI governance track for inventories, policy controls, model risk, leakage prevention, compliance mapping, and audit evidence. | B/I/A |
| 392 | Credal.ai | AI governance, model risk, privacy, and compliance | Adds Credal.ai to the AI governance track for inventories, policy controls, model risk, leakage prevention, compliance mapping, and audit evidence. | B/I/A |
| 393 | Fiddler AI | AI governance, model risk, privacy, and compliance | Adds Fiddler AI to the AI governance track for inventories, policy controls, model risk, leakage prevention, compliance mapping, and audit evidence. | B/I/A |
| 394 | Arize AI | AI governance, model risk, privacy, and compliance | Adds Arize AI to the AI governance track for inventories, policy controls, model risk, leakage prevention, compliance mapping, and audit evidence. | B/I/A |
| 395 | WhyLabs | AI governance, model risk, privacy, and compliance | Adds WhyLabs to the AI governance track for inventories, policy controls, model risk, leakage prevention, compliance mapping, and audit evidence. | B/I/A |
| 396 | Aporia | AI governance, model risk, privacy, and compliance | Adds Aporia to the AI governance track for inventories, policy controls, model risk, leakage prevention, compliance mapping, and audit evidence. | B/I/A |
| 397 | Arthur AI | AI governance, model risk, privacy, and compliance | Adds Arthur AI to the AI governance track for inventories, policy controls, model risk, leakage prevention, compliance mapping, and audit evidence. | B/I/A |
| 398 | Robust Intelligence | AI governance, model risk, privacy, and compliance | Adds Robust Intelligence to the AI governance track for inventories, policy controls, model risk, leakage prevention, compliance mapping, and audit evidence. | B/I/A |
| 399 | TruEra | AI governance, model risk, privacy, and compliance | Adds TruEra to the AI governance track for inventories, policy controls, model risk, leakage prevention, compliance mapping, and audit evidence. | B/I/A |
| 400 | ValidMind | AI governance, model risk, privacy, and compliance | Adds ValidMind to the AI governance track for inventories, policy controls, model risk, leakage prevention, compliance mapping, and audit evidence. | B/I/A |
| 401 | Procore Copilot | Architecture, construction, and real estate AI | Adds Procore Copilot to the built-environment AI track for feasibility, design generation, estimating, progress vision, schedule risk, digital twins, and property intelligence. | B/I |
| 402 | Autodesk Forma | Architecture, construction, and real estate AI | Adds Autodesk Forma to the built-environment AI track for feasibility, design generation, estimating, progress vision, schedule risk, digital twins, and property intelligence. | B/I |
| 403 | Autodesk Construction Cloud AI | Architecture, construction, and real estate AI | Adds Autodesk Construction Cloud AI to the built-environment AI track for feasibility, design generation, estimating, progress vision, schedule risk, digital twins, and property intelligence. | B/I |
| 404 | TestFit | Architecture, construction, and real estate AI | Adds TestFit to the built-environment AI track for feasibility, design generation, estimating, progress vision, schedule risk, digital twins, and property intelligence. | B/I |
| 405 | Hypar | Architecture, construction, and real estate AI | Adds Hypar to the built-environment AI track for feasibility, design generation, estimating, progress vision, schedule risk, digital twins, and property intelligence. | B/I |
| 406 | Finch | Architecture, construction, and real estate AI | Adds Finch to the built-environment AI track for feasibility, design generation, estimating, progress vision, schedule risk, digital twins, and property intelligence. | B/I |
| 407 | Archistar | Architecture, construction, and real estate AI | Adds Archistar to the built-environment AI track for feasibility, design generation, estimating, progress vision, schedule risk, digital twins, and property intelligence. | B/I |
| 408 | Maket | Architecture, construction, and real estate AI | Adds Maket to the built-environment AI track for feasibility, design generation, estimating, progress vision, schedule risk, digital twins, and property intelligence. | B/I |
| 409 | Rayon | Architecture, construction, and real estate AI | Adds Rayon to the built-environment AI track for feasibility, design generation, estimating, progress vision, schedule risk, digital twins, and property intelligence. | B/I |
| 410 | Veras | Architecture, construction, and real estate AI | Adds Veras to the built-environment AI track for feasibility, design generation, estimating, progress vision, schedule risk, digital twins, and property intelligence. | B/I |
| 411 | LookX AI | Architecture, construction, and real estate AI | Adds LookX AI to the built-environment AI track for feasibility, design generation, estimating, progress vision, schedule risk, digital twins, and property intelligence. | B/I |
| 412 | ArkDesign.ai | Architecture, construction, and real estate AI | Adds ArkDesign.ai to the built-environment AI track for feasibility, design generation, estimating, progress vision, schedule risk, digital twins, and property intelligence. | B/I |
| 413 | Cove.tool | Architecture, construction, and real estate AI | Adds Cove.tool to the built-environment AI track for feasibility, design generation, estimating, progress vision, schedule risk, digital twins, and property intelligence. | B/I |
| 414 | Togal.AI | Architecture, construction, and real estate AI | Adds Togal.AI to the built-environment AI track for feasibility, design generation, estimating, progress vision, schedule risk, digital twins, and property intelligence. | B/I |
| 415 | OpenSpace | Architecture, construction, and real estate AI | Adds OpenSpace to the built-environment AI track for feasibility, design generation, estimating, progress vision, schedule risk, digital twins, and property intelligence. | B/I |
| 416 | Buildots | Architecture, construction, and real estate AI | Adds Buildots to the built-environment AI track for feasibility, design generation, estimating, progress vision, schedule risk, digital twins, and property intelligence. | B/I |
| 417 | Doxel | Architecture, construction, and real estate AI | Adds Doxel to the built-environment AI track for feasibility, design generation, estimating, progress vision, schedule risk, digital twins, and property intelligence. | B/I |
| 418 | DroneDeploy | Architecture, construction, and real estate AI | Adds DroneDeploy to the built-environment AI track for feasibility, design generation, estimating, progress vision, schedule risk, digital twins, and property intelligence. | B/I |
| 419 | PlanRadar AI | Architecture, construction, and real estate AI | Adds PlanRadar AI to the built-environment AI track for feasibility, design generation, estimating, progress vision, schedule risk, digital twins, and property intelligence. | B/I |
| 420 | Buildxact AI | Architecture, construction, and real estate AI | Adds Buildxact AI to the built-environment AI track for feasibility, design generation, estimating, progress vision, schedule risk, digital twins, and property intelligence. | B/I |
| 421 | Slate Technologies | Architecture, construction, and real estate AI | Adds Slate Technologies to the built-environment AI track for feasibility, design generation, estimating, progress vision, schedule risk, digital twins, and property intelligence. | B/I |
| 422 | ALICE Technologies | Architecture, construction, and real estate AI | Adds ALICE Technologies to the built-environment AI track for feasibility, design generation, estimating, progress vision, schedule risk, digital twins, and property intelligence. | B/I |
| 423 | nPlan | Architecture, construction, and real estate AI | Adds nPlan to the built-environment AI track for feasibility, design generation, estimating, progress vision, schedule risk, digital twins, and property intelligence. | B/I |
| 424 | Dusty Robotics FieldPrinter | Architecture, construction, and real estate AI | Adds Dusty Robotics FieldPrinter to the built-environment AI track for feasibility, design generation, estimating, progress vision, schedule risk, digital twins, and property intelligence. | B/I |
| 425 | Matterport Property Intelligence | Architecture, construction, and real estate AI | Adds Matterport Property Intelligence to the built-environment AI track for feasibility, design generation, estimating, progress vision, schedule risk, digital twins, and property intelligence. | B/I |
| 426 | Kinaxis Maestro | Manufacturing, supply chain, logistics, and industrial AI | Adds Kinaxis Maestro to the industrial AI track for planning, inventory, predictive maintenance, quality inspection, frontline copilots, and warehouse automation. | B/I/A |
| 427 | o9 Digital Brain | Manufacturing, supply chain, logistics, and industrial AI | Adds o9 Digital Brain to the industrial AI track for planning, inventory, predictive maintenance, quality inspection, frontline copilots, and warehouse automation. | B/I/A |
| 428 | Blue Yonder | Manufacturing, supply chain, logistics, and industrial AI | Adds Blue Yonder to the industrial AI track for planning, inventory, predictive maintenance, quality inspection, frontline copilots, and warehouse automation. | B/I/A |
| 429 | ToolsGroup SO99+ | Manufacturing, supply chain, logistics, and industrial AI | Adds ToolsGroup SO99+ to the industrial AI track for planning, inventory, predictive maintenance, quality inspection, frontline copilots, and warehouse automation. | B/I/A |
| 430 | project44 Movement GPT | Manufacturing, supply chain, logistics, and industrial AI | Adds project44 Movement GPT to the industrial AI track for planning, inventory, predictive maintenance, quality inspection, frontline copilots, and warehouse automation. | B/I/A |
| 431 | FourKites Fin AI | Manufacturing, supply chain, logistics, and industrial AI | Adds FourKites Fin AI to the industrial AI track for planning, inventory, predictive maintenance, quality inspection, frontline copilots, and warehouse automation. | B/I/A |
| 432 | SAP Integrated Business Planning with Joule | Manufacturing, supply chain, logistics, and industrial AI | Adds SAP Integrated Business Planning with Joule to the industrial AI track for planning, inventory, predictive maintenance, quality inspection, frontline copilots, and warehouse automation. | B/I/A |
| 433 | Oracle Fusion Cloud SCM AI | Manufacturing, supply chain, logistics, and industrial AI | Adds Oracle Fusion Cloud SCM AI to the industrial AI track for planning, inventory, predictive maintenance, quality inspection, frontline copilots, and warehouse automation. | B/I/A |
| 434 | Infor Coleman AI | Manufacturing, supply chain, logistics, and industrial AI | Adds Infor Coleman AI to the industrial AI track for planning, inventory, predictive maintenance, quality inspection, frontline copilots, and warehouse automation. | B/I/A |
| 435 | C3 AI Reliability | Manufacturing, supply chain, logistics, and industrial AI | Adds C3 AI Reliability to the industrial AI track for planning, inventory, predictive maintenance, quality inspection, frontline copilots, and warehouse automation. | B/I/A |
| 436 | Palantir AIP for Manufacturing | Manufacturing, supply chain, logistics, and industrial AI | Adds Palantir AIP for Manufacturing to the industrial AI track for planning, inventory, predictive maintenance, quality inspection, frontline copilots, and warehouse automation. | B/I/A |
| 437 | Seeq | Manufacturing, supply chain, logistics, and industrial AI | Adds Seeq to the industrial AI track for planning, inventory, predictive maintenance, quality inspection, frontline copilots, and warehouse automation. | B/I/A |
| 438 | Augury | Manufacturing, supply chain, logistics, and industrial AI | Adds Augury to the industrial AI track for planning, inventory, predictive maintenance, quality inspection, frontline copilots, and warehouse automation. | B/I/A |
| 439 | Uptake Fusion | Manufacturing, supply chain, logistics, and industrial AI | Adds Uptake Fusion to the industrial AI track for planning, inventory, predictive maintenance, quality inspection, frontline copilots, and warehouse automation. | B/I/A |
| 440 | Siemens Industrial Copilot | Manufacturing, supply chain, logistics, and industrial AI | Adds Siemens Industrial Copilot to the industrial AI track for planning, inventory, predictive maintenance, quality inspection, frontline copilots, and warehouse automation. | B/I/A |
| 441 | PTC ThingWorx | Manufacturing, supply chain, logistics, and industrial AI | Adds PTC ThingWorx to the industrial AI track for planning, inventory, predictive maintenance, quality inspection, frontline copilots, and warehouse automation. | B/I/A |
| 442 | Rockwell FactoryTalk Analytics | Manufacturing, supply chain, logistics, and industrial AI | Adds Rockwell FactoryTalk Analytics to the industrial AI track for planning, inventory, predictive maintenance, quality inspection, frontline copilots, and warehouse automation. | B/I/A |
| 443 | Fero Labs | Manufacturing, supply chain, logistics, and industrial AI | Adds Fero Labs to the industrial AI track for planning, inventory, predictive maintenance, quality inspection, frontline copilots, and warehouse automation. | B/I/A |
| 444 | Sight Machine | Manufacturing, supply chain, logistics, and industrial AI | Adds Sight Machine to the industrial AI track for planning, inventory, predictive maintenance, quality inspection, frontline copilots, and warehouse automation. | B/I/A |
| 445 | Instrumental AI | Manufacturing, supply chain, logistics, and industrial AI | Adds Instrumental AI to the industrial AI track for planning, inventory, predictive maintenance, quality inspection, frontline copilots, and warehouse automation. | B/I/A |
| 446 | Tulip Frontline Copilot | Manufacturing, supply chain, logistics, and industrial AI | Adds Tulip Frontline Copilot to the industrial AI track for planning, inventory, predictive maintenance, quality inspection, frontline copilots, and warehouse automation. | B/I/A |
| 447 | LandingLens | Manufacturing, supply chain, logistics, and industrial AI | Adds LandingLens to the industrial AI track for planning, inventory, predictive maintenance, quality inspection, frontline copilots, and warehouse automation. | B/I/A |
| 448 | Robovision AI | Manufacturing, supply chain, logistics, and industrial AI | Adds Robovision AI to the industrial AI track for planning, inventory, predictive maintenance, quality inspection, frontline copilots, and warehouse automation. | B/I/A |
| 449 | GreyOrange GreyMatter | Manufacturing, supply chain, logistics, and industrial AI | Adds GreyOrange GreyMatter to the industrial AI track for planning, inventory, predictive maintenance, quality inspection, frontline copilots, and warehouse automation. | B/I/A |
| 450 | LocusONE | Manufacturing, supply chain, logistics, and industrial AI | Adds LocusONE to the industrial AI track for planning, inventory, predictive maintenance, quality inspection, frontline copilots, and warehouse automation. | B/I/A |
| 451 | AlphaFold Server | Scientific, biotech, lab, and clinical AI | Adds AlphaFold Server to the scientific and clinical AI track for drug discovery, lab informatics, imaging AI, evidence limits, validation, and safety. | B/I/A |
| 452 | Isomorphic Labs Drug Design Engine | Scientific, biotech, lab, and clinical AI | Adds Isomorphic Labs Drug Design Engine to the scientific and clinical AI track for drug discovery, lab informatics, imaging AI, evidence limits, validation, and safety. | B/I/A |
| 453 | NVIDIA BioNeMo | Scientific, biotech, lab, and clinical AI | Adds NVIDIA BioNeMo to the scientific and clinical AI track for drug discovery, lab informatics, imaging AI, evidence limits, validation, and safety. | B/I/A |
| 454 | AWS Bio Discovery | Scientific, biotech, lab, and clinical AI | Adds AWS Bio Discovery to the scientific and clinical AI track for drug discovery, lab informatics, imaging AI, evidence limits, validation, and safety. | B/I/A |
| 455 | Benchling AI | Scientific, biotech, lab, and clinical AI | Adds Benchling AI to the scientific and clinical AI track for drug discovery, lab informatics, imaging AI, evidence limits, validation, and safety. | B/I/A |
| 456 | Scispot | Scientific, biotech, lab, and clinical AI | Adds Scispot to the scientific and clinical AI track for drug discovery, lab informatics, imaging AI, evidence limits, validation, and safety. | B/I/A |
| 457 | Sapio Sciences | Scientific, biotech, lab, and clinical AI | Adds Sapio Sciences to the scientific and clinical AI track for drug discovery, lab informatics, imaging AI, evidence limits, validation, and safety. | B/I/A |
| 458 | Dotmatics Luma | Scientific, biotech, lab, and clinical AI | Adds Dotmatics Luma to the scientific and clinical AI track for drug discovery, lab informatics, imaging AI, evidence limits, validation, and safety. | B/I/A |
| 459 | Schrödinger LiveDesign | Scientific, biotech, lab, and clinical AI | Adds Schrödinger LiveDesign to the scientific and clinical AI track for drug discovery, lab informatics, imaging AI, evidence limits, validation, and safety. | B/I/A |
| 460 | OpenEye Orion | Scientific, biotech, lab, and clinical AI | Adds OpenEye Orion to the scientific and clinical AI track for drug discovery, lab informatics, imaging AI, evidence limits, validation, and safety. | B/I/A |
| 461 | CDD Vault | Scientific, biotech, lab, and clinical AI | Adds CDD Vault to the scientific and clinical AI track for drug discovery, lab informatics, imaging AI, evidence limits, validation, and safety. | B/I/A |
| 462 | Recursion OS | Scientific, biotech, lab, and clinical AI | Adds Recursion OS to the scientific and clinical AI track for drug discovery, lab informatics, imaging AI, evidence limits, validation, and safety. | B/I/A |
| 463 | Insilico Medicine Pharma.AI | Scientific, biotech, lab, and clinical AI | Adds Insilico Medicine Pharma.AI to the scientific and clinical AI track for drug discovery, lab informatics, imaging AI, evidence limits, validation, and safety. | B/I/A |
| 464 | BenevolentAI | Scientific, biotech, lab, and clinical AI | Adds BenevolentAI to the scientific and clinical AI track for drug discovery, lab informatics, imaging AI, evidence limits, validation, and safety. | B/I/A |
| 465 | Exscientia | Scientific, biotech, lab, and clinical AI | Adds Exscientia to the scientific and clinical AI track for drug discovery, lab informatics, imaging AI, evidence limits, validation, and safety. | B/I/A |
| 466 | Atomwise | Scientific, biotech, lab, and clinical AI | Adds Atomwise to the scientific and clinical AI track for drug discovery, lab informatics, imaging AI, evidence limits, validation, and safety. | B/I/A |
| 467 | Iktos Makya | Scientific, biotech, lab, and clinical AI | Adds Iktos Makya to the scientific and clinical AI track for drug discovery, lab informatics, imaging AI, evidence limits, validation, and safety. | B/I/A |
| 468 | Valo Opal | Scientific, biotech, lab, and clinical AI | Adds Valo Opal to the scientific and clinical AI track for drug discovery, lab informatics, imaging AI, evidence limits, validation, and safety. | B/I/A |
| 469 | Owkin K | Scientific, biotech, lab, and clinical AI | Adds Owkin K to the scientific and clinical AI track for drug discovery, lab informatics, imaging AI, evidence limits, validation, and safety. | B/I/A |
| 470 | PathAI AISight | Scientific, biotech, lab, and clinical AI | Adds PathAI AISight to the scientific and clinical AI track for drug discovery, lab informatics, imaging AI, evidence limits, validation, and safety. | B/I/A |
| 471 | Paige | Scientific, biotech, lab, and clinical AI | Adds Paige to the scientific and clinical AI track for drug discovery, lab informatics, imaging AI, evidence limits, validation, and safety. | B/I/A |
| 472 | Tempus One | Scientific, biotech, lab, and clinical AI | Adds Tempus One to the scientific and clinical AI track for drug discovery, lab informatics, imaging AI, evidence limits, validation, and safety. | B/I/A |
| 473 | Viz.ai | Scientific, biotech, lab, and clinical AI | Adds Viz.ai to the scientific and clinical AI track for drug discovery, lab informatics, imaging AI, evidence limits, validation, and safety. | B/I/A |
| 474 | Aidoc | Scientific, biotech, lab, and clinical AI | Adds Aidoc to the scientific and clinical AI track for drug discovery, lab informatics, imaging AI, evidence limits, validation, and safety. | B/I/A |
| 475 | Qure.ai | Scientific, biotech, lab, and clinical AI | Adds Qure.ai to the scientific and clinical AI track for drug discovery, lab informatics, imaging AI, evidence limits, validation, and safety. | B/I/A |
| 476 | Granola | Personal productivity, notes, email, calendar, and knowledge AI | Adds Granola to the personal productivity AI track for knowledge management, email triage, calendar agents, meeting memory, voice capture, and cognitive offloading. | B/I |
| 477 | Superhuman AI | Personal productivity, notes, email, calendar, and knowledge AI | Adds Superhuman AI to the personal productivity AI track for knowledge management, email triage, calendar agents, meeting memory, voice capture, and cognitive offloading. | B/I |
| 478 | Shortwave | Personal productivity, notes, email, calendar, and knowledge AI | Adds Shortwave to the personal productivity AI track for knowledge management, email triage, calendar agents, meeting memory, voice capture, and cognitive offloading. | B/I |
| 479 | Fyxer AI | Personal productivity, notes, email, calendar, and knowledge AI | Adds Fyxer AI to the personal productivity AI track for knowledge management, email triage, calendar agents, meeting memory, voice capture, and cognitive offloading. | B/I |
| 480 | Motion | Personal productivity, notes, email, calendar, and knowledge AI | Adds Motion to the personal productivity AI track for knowledge management, email triage, calendar agents, meeting memory, voice capture, and cognitive offloading. | B/I |
| 481 | Reclaim.ai | Personal productivity, notes, email, calendar, and knowledge AI | Adds Reclaim.ai to the personal productivity AI track for knowledge management, email triage, calendar agents, meeting memory, voice capture, and cognitive offloading. | B/I |
| 482 | Clockwise | Personal productivity, notes, email, calendar, and knowledge AI | Adds Clockwise to the personal productivity AI track for knowledge management, email triage, calendar agents, meeting memory, voice capture, and cognitive offloading. | B/I |
| 483 | Akiflow | Personal productivity, notes, email, calendar, and knowledge AI | Adds Akiflow to the personal productivity AI track for knowledge management, email triage, calendar agents, meeting memory, voice capture, and cognitive offloading. | B/I |
| 484 | Mem | Personal productivity, notes, email, calendar, and knowledge AI | Adds Mem to the personal productivity AI track for knowledge management, email triage, calendar agents, meeting memory, voice capture, and cognitive offloading. | B/I |
| 485 | Tana | Personal productivity, notes, email, calendar, and knowledge AI | Adds Tana to the personal productivity AI track for knowledge management, email triage, calendar agents, meeting memory, voice capture, and cognitive offloading. | B/I |
| 486 | Reflect AI | Personal productivity, notes, email, calendar, and knowledge AI | Adds Reflect AI to the personal productivity AI track for knowledge management, email triage, calendar agents, meeting memory, voice capture, and cognitive offloading. | B/I |
| 487 | Obsidian Copilot | Personal productivity, notes, email, calendar, and knowledge AI | Adds Obsidian Copilot to the personal productivity AI track for knowledge management, email triage, calendar agents, meeting memory, voice capture, and cognitive offloading. | B/I |
| 488 | Capacities AI | Personal productivity, notes, email, calendar, and knowledge AI | Adds Capacities AI to the personal productivity AI track for knowledge management, email triage, calendar agents, meeting memory, voice capture, and cognitive offloading. | B/I |
| 489 | Readwise Reader Ghostreader | Personal productivity, notes, email, calendar, and knowledge AI | Adds Readwise Reader Ghostreader to the personal productivity AI track for knowledge management, email triage, calendar agents, meeting memory, voice capture, and cognitive offloading. | B/I |
| 490 | Saner.AI | Personal productivity, notes, email, calendar, and knowledge AI | Adds Saner.AI to the personal productivity AI track for knowledge management, email triage, calendar agents, meeting memory, voice capture, and cognitive offloading. | B/I |
| 491 | Jamie | Personal productivity, notes, email, calendar, and knowledge AI | Adds Jamie to the personal productivity AI track for knowledge management, email triage, calendar agents, meeting memory, voice capture, and cognitive offloading. | B/I |
| 492 | Limitless | Personal productivity, notes, email, calendar, and knowledge AI | Adds Limitless to the personal productivity AI track for knowledge management, email triage, calendar agents, meeting memory, voice capture, and cognitive offloading. | B/I |
| 493 | PLAUD Note | Personal productivity, notes, email, calendar, and knowledge AI | Adds PLAUD Note to the personal productivity AI track for knowledge management, email triage, calendar agents, meeting memory, voice capture, and cognitive offloading. | B/I |
| 494 | Wispr Flow | Personal productivity, notes, email, calendar, and knowledge AI | Adds Wispr Flow to the personal productivity AI track for knowledge management, email triage, calendar agents, meeting memory, voice capture, and cognitive offloading. | B/I |
| 495 | Notability AI | Personal productivity, notes, email, calendar, and knowledge AI | Adds Notability AI to the personal productivity AI track for knowledge management, email triage, calendar agents, meeting memory, voice capture, and cognitive offloading. | B/I |
| 496 | Evernote AI | Personal productivity, notes, email, calendar, and knowledge AI | Adds Evernote AI to the personal productivity AI track for knowledge management, email triage, calendar agents, meeting memory, voice capture, and cognitive offloading. | B/I |
| 497 | Craft AI | Personal productivity, notes, email, calendar, and knowledge AI | Adds Craft AI to the personal productivity AI track for knowledge management, email triage, calendar agents, meeting memory, voice capture, and cognitive offloading. | B/I |
| 498 | Logseq AI | Personal productivity, notes, email, calendar, and knowledge AI | Adds Logseq AI to the personal productivity AI track for knowledge management, email triage, calendar agents, meeting memory, voice capture, and cognitive offloading. | B/I |
| 499 | Anytype AI | Personal productivity, notes, email, calendar, and knowledge AI | Adds Anytype AI to the personal productivity AI track for knowledge management, email triage, calendar agents, meeting memory, voice capture, and cognitive offloading. | B/I |
| 500 | Knapsack AI | Personal productivity, notes, email, calendar, and knowledge AI | Adds Knapsack AI to the personal productivity AI track for knowledge management, email triage, calendar agents, meeting memory, voice capture, and cognitive offloading. | B/I |

## Page Design Notes for `/theladder-products`

- The page should not copy the 15-tier Ladder. It should be a catalog pathway: category rail, product cards, and course depth filters.
- A learner should be able to start with a product they already use, then branch into concept courses that explain what is happening underneath.
- Product courses should use the same assignment-lab pattern as the Ladder: every course includes a debate, skill drill, or build task.
- `B/I/A` products should become three separate course nodes. `B/I` products should become two nodes. `B` products should remain single orientation courses.
- The catalog should support updates because product adoption changes quickly.

## Initial Build Recommendation

Start `/theladder-products` with these filters:

- Product type
- Beginner/intermediate/advanced
- Consumer, workplace, developer, enterprise, regulated
- Free/paid/enterprise
- Uses files, uses web, uses images, uses voice/video, uses databases, uses agents
- Requires account, requires payment, requires business approval

First release should expose all 250 products as cards, but only fully write the first 25 course outlines. The rest can be marked "planned" until the course scaffold is generated.
