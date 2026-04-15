#!/usr/bin/env python3
"""Translate /es/ and /hi/ shell pages from English sources.

Strategy: start from the canonical English source file, apply a language-specific
string-substitution table, write to the target. Idempotent — rerunning regenerates
the same output from canonical English.

Brand names kept in English: AESOP, AI Academy, AESOP AI Academy, Discord,
AesopAcademy.org, ADA, Swiss Army Knife, Claude AI, Scott Schindler.
"""
import re, sys, pathlib

ROOT = pathlib.Path("/sessions/epic-inspiring-wozniak/mnt/Aesop")

# ───────── Spanish translations ─────────
ES = [
    # <title> / <meta description>
    ("AESOP AI Academy — AI Literacy Curriculum for Ages 5+",
     "AESOP AI Academy — Currículo de Alfabetización en IA para Mayores de 5 Años"),
    ("AESOP AI Academy delivers the first story-driven AI literacy curriculum for ages 5+. Three courses — Intro, Basic, and Advanced — covering AI concepts, ethics, safety, and future careers — powered by the AESOP storytelling engine.",
     "AESOP AI Academy ofrece el primer currículo de alfabetización en IA basado en narrativas para mayores de 5 años. Tres cursos — Introducción, Básico y Avanzado — que cubren conceptos de IA, ética, seguridad y carreras del futuro, impulsado por el motor de narrativa AESOP."),
    # Nav
    (">AI News<", ">Noticias de IA<"),
    (">Forums - Discord<", ">Foros - Discord<"),
    ("⚑ Report Issue", "⚑ Reportar Problema"),
    ('aria-label="Open menu"', 'aria-label="Abrir menú"'),
    ('aria-label="Toggle dark mode"', 'aria-label="Modo oscuro"'),
    ('title="Toggle dark mode"', 'title="Alternar modo oscuro"'),
    # Hero
    ("AESOP (Patent Pending) — Gamified Learning Engine",
     "AESOP (Patente en Trámite) — Motor de Aprendizaje Gamificado"),
    ("Learning through Adventure, Exploration, Storytelling,<br>and Open-Minded Play",
     "Aprendizaje a través de Aventura, Exploración, Narrativa<br>y Juego de Mente Abierta"),
    ("The first AI literacy curriculum where <strong>the AI is not just the subject — it's the classroom.</strong>",
     "El primer currículo de alfabetización en IA donde <strong>la IA no es solo el tema — es el aula.</strong>"),
    ("Three courses — Intro, Basic, and Advanced — covering what AI is, how to use it responsibly, AI safety &amp; ethics, storytelling with AI, and future careers.",
     "Tres cursos — Introducción, Básico y Avanzado — que cubren qué es la IA, cómo usarla responsablemente, seguridad y ética de la IA, narrativa con IA y carreras del futuro."),
    ("Enter AI Academy →", "Entrar a AI Academy →"),
    ("Join the Community", "Únete a la Comunidad"),
    # Side cards
    (">External Reviews<", ">Reseñas Externas<"),
    (">AESOP Training Scores<", ">Puntuaciones de Entrenamiento AESOP<"),
    (">Accessibility<", ">Accesibilidad<"),
    (">ADA Policy<", ">Política ADA<"),
    (">Governance<", ">Gobernanza<"),
    (">AI Policy<", ">Política de IA<"),
    (">Little Professor<", ">Pequeño Profesor<"),
    (">Teacher / Parent Dashboard<", ">Panel de Maestros / Padres<"),
    # Pull quotes
    ("\"The first AI literacy curriculum where AI is not just the subject —<br><em style=\"color:var(--gold-light);font-style:normal;\">it's the classroom.</em>\"",
     "\"El primer currículo de alfabetización en IA donde la IA no es solo el tema —<br><em style=\"color:var(--gold-light);font-style:normal;\">es el aula.</em>\""),
    ("\"AI isn't the outcome.<br>It's a really big<br><em style=\"color:var(--gold-light);font-style:normal;\">Swiss Army Knife.</em>\"",
     "\"La IA no es el resultado.<br>Es una enorme<br><em style=\"color:var(--gold-light);font-style:normal;\">Navaja Suiza.</em>\""),
    # Footer
    ("Story-driven AI literacy for every age.<br>\n        Built by educators. Powered by AESOP.",
     "Alfabetización en IA basada en narrativas para toda edad.<br>\n        Creado por educadores. Impulsado por AESOP."),
    (">AI Academy</a>", ">AI Academy</a>"),  # brand keep
    (">Site Map<", ">Mapa del Sitio<"),
    ("© 2026 AESOP AI Academy — All Rights Reserved",
     "© 2026 AESOP AI Academy — Todos los Derechos Reservados"),
    ("AESOP Engine — Patent Pending · App #64/018,565",
     "Motor AESOP — Patente en Trámite · Solicitud #64/018,565"),
    # Dev banner
    ('title="Click to dismiss"', 'title="Clic para descartar"'),
    ("⚠&nbsp; We are in DEVELOPMENT. &nbsp;Many site features may not work. &nbsp;⚠",
     "⚠&nbsp; Estamos en DESARROLLO. &nbsp;Muchas funciones del sitio pueden no funcionar. &nbsp;⚠"),
    # Hub-specific strings (ai-academy/index.html)
    ("AI Academy — Your Learning Path",
     "AI Academy — Tu Camino de Aprendizaje"),
    ("Three tiers of learning across ten modules.",
     "Tres niveles de aprendizaje a través de diez módulos."),
    (">Intro<", ">Introducción<"),
    (">Basic<", ">Básico<"),
    (">Advanced<", ">Avanzado<"),
    # Hub: AGE_GROUPS tier labels & descriptions
    ('label:"Parent & Teacher Orientation"', 'label:"Orientación para Padres y Maestros"'),
    ('label:"Introduction"', 'label:"Introducción"'),
    ('label:"Basic"', 'label:"Básico"'),
    ('label:"Advanced"', 'label:"Avanzado"'),
    ('desc:"Introduction to AI Foundations & Youth Education. Explore what AI is through story, curiosity, and hands-on discovery."',
     'desc:"Introducción a los Fundamentos de IA y Educación Juvenil. Explora qué es la IA a través de historias, curiosidad y descubrimiento práctico."'),
    ('desc:"Basic AI Foundations & Young Adult Education. Go deeper into how AI works, where it fails, and what it means for your world."',
     'desc:"Fundamentos Básicos de IA y Educación para Jóvenes Adultos. Profundiza en cómo funciona la IA, dónde falla y qué significa para tu mundo."'),
    ('desc:"Advanced AI Foundations & Adult Education. The full master track — technical depth, ethics at scale, and your AI career launchpad."',
     'desc:"Fundamentos Avanzados de IA y Educación para Adultos. La ruta maestra completa — profundidad técnica, ética a escala y tu plataforma de lanzamiento profesional en IA."'),
    # Hub: MODULE titles (10) + descriptions
    ('title:"What AI Is"', 'title:"Qué Es la IA"'),
    ('title:"AI in Our World"', 'title:"La IA en Nuestro Mundo"'),
    ('title:"Sometimes AI Gets It Wrong"', 'title:"A Veces la IA Se Equivoca"'),
    ('title:"Stories & Creativity with AI"', 'title:"Historias y Creatividad con IA"'),
    ('title:"Staying Safe with AI"', 'title:"Estar Seguro con la IA"'),
    ('title:"How AI Learns"', 'title:"Cómo Aprende la IA"'),
    ('title:"How AI Thinks"', 'title:"Cómo Piensa la IA"'),
    ('title:"AI Ethics & Real Decisions"', 'title:"Ética de la IA y Decisiones Reales"'),
    ('title:"AI and the Future"', 'title:"La IA y el Futuro"'),
    ('title:"Building with AI"', 'title:"Construir con IA"'),
    ('desc:"Foundation concepts: defining AI, distinguishing it from magic and human thinking, real examples."',
     'desc:"Conceptos fundamentales: definir la IA, distinguirla de la magia y del pensamiento humano, ejemplos reales."'),
    ('desc:"AI applications across industries, daily life, and society — from toys to hospitals."',
     'desc:"Aplicaciones de la IA en industrias, vida diaria y sociedad — desde juguetes hasta hospitales."'),
    ('desc:"Errors, hallucinations, bias, and limits — building critical thinking about AI outputs."',
     'desc:"Errores, alucinaciones, sesgo y límites — desarrollar pensamiento crítico sobre las salidas de la IA."'),
    ('desc:"AI as creative collaborator — storytelling, art, music, play, and imaginative expression."',
     'desc:"La IA como colaborador creativo — narrativa, arte, música, juego y expresión imaginativa."'),
    ('desc:"Privacy, safety, responsible use, and digital citizenship when interacting with AI."',
     'desc:"Privacidad, seguridad, uso responsable y ciudadanía digital al interactuar con la IA."'),
    ('desc:"The mechanics of machine learning — data, training, models, and what \'learning\' really means."',
     'desc:"La mecánica del aprendizaje automático — datos, entrenamiento, modelos y qué significa realmente \'aprender\'."'),
    ('desc:"Inside the inference process — how AI processes input, generates output, and where it breaks."',
     'desc:"Dentro del proceso de inferencia — cómo la IA procesa entradas, genera salidas y dónde falla."'),
    ('desc:"Ethical frameworks applied to real AI decisions — who decides, who is harmed, who benefits."',
     'desc:"Marcos éticos aplicados a decisiones reales de IA — quién decide, quién resulta perjudicado, quién se beneficia."'),
    ('desc:"Long-term trajectories, existential questions, democratic futures, and the choices that remain."',
     'desc:"Trayectorias a largo plazo, preguntas existenciales, futuros democráticos y las decisiones que quedan."'),
    ('desc:"Practical frameworks for designing, evaluating, and responsibly deploying AI systems."',
     'desc:"Marcos prácticos para diseñar, evaluar e implementar responsablemente sistemas de IA."'),
    # Hub UI labels
    ('Select a Course to Begin', 'Selecciona un Curso para Comenzar'),
    ('Modules</span>', 'Módulos</span>'),
    ('Lessons</span>', 'Lecciones</span>'),
    ('Module ${i + 1}', 'Módulo ${i + 1}'),
    ('${g.modulesUnlocked} Modules', '${g.modulesUnlocked} Módulos'),
    ('${totalL} Lessons', '${totalL} Lecciones'),
    # Placeholder comment strip (the clone marker)
    ("<!-- ═══════════════════════════════════════════════════════════════════════════\n     SPANISH PAGE — TRANSLATION PLACEHOLDER\n     This file is a structural clone of /index.html. All visible copy is still\n     English, pending Spanish translations supplied by the owner. Do not\n     diverge structurally from the English source without also updating it.\n     ═══════════════════════════════════════════════════════════════════════════ -->\n\n",
     ""),
]

# ───────── Hindi translations ─────────
HI = [
    ("AESOP AI Academy — AI Literacy Curriculum for Ages 5+",
     "AESOP AI Academy — 5+ आयु के लिए AI साक्षरता पाठ्यक्रम"),
    ("AESOP AI Academy delivers the first story-driven AI literacy curriculum for ages 5+. Three courses — Intro, Basic, and Advanced — covering AI concepts, ethics, safety, and future careers — powered by the AESOP storytelling engine.",
     "AESOP AI Academy 5+ आयु के लिए पहला कहानी-संचालित AI साक्षरता पाठ्यक्रम प्रदान करता है। तीन पाठ्यक्रम — प्रारंभिक, बुनियादी, और उन्नत — AI अवधारणाओं, नैतिकता, सुरक्षा, और भविष्य के करियर को कवर करते हैं, AESOP कहानी इंजन द्वारा संचालित।"),
    (">AI News<", ">AI समाचार<"),
    (">Forums - Discord<", ">फोरम - Discord<"),
    ("⚑ Report Issue", "⚑ समस्या रिपोर्ट करें"),
    ('aria-label="Open menu"', 'aria-label="मेनू खोलें"'),
    ('aria-label="Toggle dark mode"', 'aria-label="डार्क मोड"'),
    ('title="Toggle dark mode"', 'title="डार्क मोड टॉगल करें"'),
    ("AESOP (Patent Pending) — Gamified Learning Engine",
     "AESOP (पेटेंट लंबित) — गेमिफाइड लर्निंग इंजन"),
    ("Learning through Adventure, Exploration, Storytelling,<br>and Open-Minded Play",
     "साहसिक कार्य, अन्वेषण, कहानी कहने<br>और खुले मन से खेल के माध्यम से सीखना"),
    ("The first AI literacy curriculum where <strong>the AI is not just the subject — it's the classroom.</strong>",
     "पहला AI साक्षरता पाठ्यक्रम जहाँ <strong>AI केवल विषय नहीं है — यह कक्षा है।</strong>"),
    ("Three courses — Intro, Basic, and Advanced — covering what AI is, how to use it responsibly, AI safety &amp; ethics, storytelling with AI, and future careers.",
     "तीन पाठ्यक्रम — प्रारंभिक, बुनियादी, और उन्नत — AI क्या है, इसे जिम्मेदारी से कैसे उपयोग करें, AI सुरक्षा और नैतिकता, AI के साथ कहानी कहना, और भविष्य के करियर को कवर करते हैं।"),
    ("Enter AI Academy →", "AI Academy में प्रवेश करें →"),
    ("Join the Community", "समुदाय में शामिल हों"),
    (">External Reviews<", ">बाहरी समीक्षाएँ<"),
    (">AESOP Training Scores<", ">AESOP प्रशिक्षण स्कोर<"),
    (">Accessibility<", ">सुगम्यता<"),
    (">ADA Policy<", ">ADA नीति<"),
    (">Governance<", ">शासन<"),
    (">AI Policy<", ">AI नीति<"),
    (">Little Professor<", ">छोटे प्रोफेसर<"),
    (">Teacher / Parent Dashboard<", ">शिक्षक / अभिभावक डैशबोर्ड<"),
    ("\"The first AI literacy curriculum where AI is not just the subject —<br><em style=\"color:var(--gold-light);font-style:normal;\">it's the classroom.</em>\"",
     "\"पहला AI साक्षरता पाठ्यक्रम जहाँ AI केवल विषय नहीं है —<br><em style=\"color:var(--gold-light);font-style:normal;\">यह कक्षा है।</em>\""),
    ("\"AI isn't the outcome.<br>It's a really big<br><em style=\"color:var(--gold-light);font-style:normal;\">Swiss Army Knife.</em>\"",
     "\"AI परिणाम नहीं है।<br>यह एक बहुत बड़ा<br><em style=\"color:var(--gold-light);font-style:normal;\">स्विस आर्मी चाकू है।</em>\""),
    ("Story-driven AI literacy for every age.<br>\n        Built by educators. Powered by AESOP.",
     "हर आयु के लिए कहानी-संचालित AI साक्षरता।<br>\n        शिक्षकों द्वारा निर्मित। AESOP द्वारा संचालित।"),
    (">Site Map<", ">साइट मैप<"),
    ("© 2026 AESOP AI Academy — All Rights Reserved",
     "© 2026 AESOP AI Academy — सर्वाधिकार सुरक्षित"),
    ("AESOP Engine — Patent Pending · App #64/018,565",
     "AESOP इंजन — पेटेंट लंबित · आवेदन #64/018,565"),
    ('title="Click to dismiss"', 'title="बंद करने के लिए क्लिक करें"'),
    ("⚠&nbsp; We are in DEVELOPMENT. &nbsp;Many site features may not work. &nbsp;⚠",
     "⚠&nbsp; हम विकासाधीन हैं। &nbsp;साइट की कई सुविधाएँ काम नहीं कर सकती हैं। &nbsp;⚠"),
    ("AI Academy — Your Learning Path",
     "AI Academy — आपका सीखने का मार्ग"),
    ("Three tiers of learning across ten modules.",
     "दस मॉड्यूल में सीखने के तीन स्तर।"),
    (">Intro<", ">प्रारंभिक<"),
    (">Basic<", ">बुनियादी<"),
    (">Advanced<", ">उन्नत<"),
    # Hub tier labels
    ('label:"Parent & Teacher Orientation"', 'label:"अभिभावक और शिक्षक अभिविन्यास"'),
    ('label:"Introduction"', 'label:"परिचय"'),
    ('label:"Basic"', 'label:"बुनियादी"'),
    ('label:"Advanced"', 'label:"उन्नत"'),
    ('desc:"Introduction to AI Foundations & Youth Education. Explore what AI is through story, curiosity, and hands-on discovery."',
     'desc:"AI बुनियादी बातों और युवा शिक्षा का परिचय। कहानी, जिज्ञासा और व्यावहारिक खोज के माध्यम से जानें कि AI क्या है।"'),
    ('desc:"Basic AI Foundations & Young Adult Education. Go deeper into how AI works, where it fails, and what it means for your world."',
     'desc:"बुनियादी AI आधार और युवा वयस्क शिक्षा। गहराई में जाएँ कि AI कैसे काम करता है, कहाँ विफल होता है, और आपकी दुनिया के लिए इसका क्या अर्थ है।"'),
    ('desc:"Advanced AI Foundations & Adult Education. The full master track — technical depth, ethics at scale, and your AI career launchpad."',
     'desc:"उन्नत AI आधार और वयस्क शिक्षा। पूर्ण मास्टर ट्रैक — तकनीकी गहराई, बड़े पैमाने पर नैतिकता, और आपका AI करियर लॉन्चपैड।"'),
    # Hub MODULE titles
    ('title:"What AI Is"', 'title:"AI क्या है"'),
    ('title:"AI in Our World"', 'title:"हमारी दुनिया में AI"'),
    ('title:"Sometimes AI Gets It Wrong"', 'title:"कभी-कभी AI गलत होता है"'),
    ('title:"Stories & Creativity with AI"', 'title:"AI के साथ कहानियाँ और रचनात्मकता"'),
    ('title:"Staying Safe with AI"', 'title:"AI के साथ सुरक्षित रहना"'),
    ('title:"How AI Learns"', 'title:"AI कैसे सीखता है"'),
    ('title:"How AI Thinks"', 'title:"AI कैसे सोचता है"'),
    ('title:"AI Ethics & Real Decisions"', 'title:"AI नैतिकता और वास्तविक निर्णय"'),
    ('title:"AI and the Future"', 'title:"AI और भविष्य"'),
    ('title:"Building with AI"', 'title:"AI के साथ निर्माण"'),
    ('desc:"Foundation concepts: defining AI, distinguishing it from magic and human thinking, real examples."',
     'desc:"बुनियादी अवधारणाएँ: AI को परिभाषित करना, इसे जादू और मानवीय सोच से अलग करना, वास्तविक उदाहरण।"'),
    ('desc:"AI applications across industries, daily life, and society — from toys to hospitals."',
     'desc:"उद्योगों, दैनिक जीवन और समाज में AI के अनुप्रयोग — खिलौनों से लेकर अस्पतालों तक।"'),
    ('desc:"Errors, hallucinations, bias, and limits — building critical thinking about AI outputs."',
     'desc:"त्रुटियाँ, मतिभ्रम, पक्षपात और सीमाएँ — AI आउटपुट पर आलोचनात्मक सोच का निर्माण।"'),
    ('desc:"AI as creative collaborator — storytelling, art, music, play, and imaginative expression."',
     'desc:"रचनात्मक सहयोगी के रूप में AI — कहानी कहना, कला, संगीत, खेल और कल्पनाशील अभिव्यक्ति।"'),
    ('desc:"Privacy, safety, responsible use, and digital citizenship when interacting with AI."',
     'desc:"AI के साथ बातचीत करते समय गोपनीयता, सुरक्षा, जिम्मेदार उपयोग और डिजिटल नागरिकता।"'),
    ('desc:"The mechanics of machine learning — data, training, models, and what \'learning\' really means."',
     'desc:"मशीन लर्निंग की यांत्रिकी — डेटा, प्रशिक्षण, मॉडल, और \'सीखने\' का वास्तव में क्या अर्थ है।"'),
    ('desc:"Inside the inference process — how AI processes input, generates output, and where it breaks."',
     'desc:"अनुमान प्रक्रिया के अंदर — AI कैसे इनपुट प्रोसेस करता है, आउटपुट उत्पन्न करता है, और कहाँ टूटता है।"'),
    ('desc:"Ethical frameworks applied to real AI decisions — who decides, who is harmed, who benefits."',
     'desc:"वास्तविक AI निर्णयों पर लागू नैतिक ढाँचे — कौन निर्णय लेता है, कौन हानि उठाता है, कौन लाभान्वित होता है।"'),
    ('desc:"Long-term trajectories, existential questions, democratic futures, and the choices that remain."',
     'desc:"दीर्घकालिक प्रक्षेप पथ, अस्तित्वगत प्रश्न, लोकतांत्रिक भविष्य, और शेष विकल्प।"'),
    ('desc:"Practical frameworks for designing, evaluating, and responsibly deploying AI systems."',
     'desc:"AI सिस्टम डिजाइन करने, मूल्यांकन करने, और जिम्मेदारी से तैनात करने के लिए व्यावहारिक ढाँचे।"'),
    ('Select a Course to Begin', 'शुरू करने के लिए एक पाठ्यक्रम चुनें'),
    ('Modules</span>', 'मॉड्यूल</span>'),
    ('Lessons</span>', 'पाठ</span>'),
    ('Module ${i + 1}', 'मॉड्यूल ${i + 1}'),
    ('${g.modulesUnlocked} Modules', '${g.modulesUnlocked} मॉड्यूल'),
    ('${totalL} Lessons', '${totalL} पाठ'),
    ("<!-- ═══════════════════════════════════════════════════════════════════════════\n     SPANISH PAGE — TRANSLATION PLACEHOLDER\n     This file is a structural clone of /index.html. All visible copy is still\n     English, pending Spanish translations supplied by the owner. Do not\n     diverge structurally from the English source without also updating it.\n     ═══════════════════════════════════════════════════════════════════════════ -->\n\n",
     ""),
]

def apply(src_path, subs, lang):
    txt = pathlib.Path(src_path).read_text(encoding="utf-8")
    # Always set html lang
    txt = re.sub(r'<html lang="[a-z\-]+">', f'<html lang="{lang}">', txt, count=1)
    hits = 0
    for a, b in subs:
        if a in txt:
            txt = txt.replace(a, b)
            hits += 1
    return txt, hits

def translate(src_rel, tgt_rel, subs, lang):
    src = ROOT / src_rel
    tgt = ROOT / tgt_rel
    txt, hits = apply(src, subs, lang)
    tgt.parent.mkdir(parents=True, exist_ok=True)
    tgt.write_text(txt, encoding="utf-8")
    print(f"  {tgt_rel}: {hits}/{len(subs)} substitutions applied ({len(txt)}b)")

for lang, subs in [("es", ES), ("hi", HI)]:
    print(f"\n=== {lang.upper()} ===")
    translate("index.html", f"{lang}/index.html", subs, lang)
    translate("ai-academy/index.html", f"{lang}/ai-academy/index.html", subs, lang)
print("\nDone.")
