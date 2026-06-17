BG_TOP = (6, 28, 14)
BG_BOT = (2, 10, 6)
GOLD = (212, 175, 55)
GOLD_LIGHT = (240, 210, 100)
GOLD_DIM = (140, 115, 35)
FOREST = (34, 100, 50)
FOREST_DARK = (18, 50, 28)
CARD_BG = (14, 38, 22)
CARD_BORDER = (30, 70, 40)
CARD_HOVER_COL = (22, 55, 35)
ACCENT_ORANGE = (255, 140, 0)
DANGER = (200, 50, 50)
DANGER_LIGHT = (230, 80, 80)
TEXT_COLOR = (235, 225, 205)
TEXT_DIM = (160, 150, 130)
PARCHMENT = (245, 235, 215)
PARCHMENT_DARK = (200, 185, 160)
HUD_BG = (10, 30, 18, 180)


CHAPTERS_DATA = [
    {
        "name": "Capítulo 1: Lenda do Guaraná",
        "rank": "Aprendiz",
        "color": FOREST,
        "paragraphs": [
            {"id": "A", "text": "Toda a tribo xorou muito a perda da criança. Tupã se compadeceu do terrível zacrifício e enviou uma mensagem aos pajés."},
            {"id": "B", "text": "Há muito tempo, numa aldeia na floresta, vivia um indiozinho muito querido. Ele trazia muita alegria e forca para o seu povo."},
            {"id": "C", "text": "A mãe plantou os olhos do menino na terra fértil. Ali nasceu uma planta nova, cujas sementes parecem olhos: o guaraná."},
            {"id": "D", "text": "Jurupari, o espírito do mal, sentiu inveja da criança e se transformou em uma serpente poderoza para atacá-la na floresta."}
        ],
        "correct_order": ["B", "D", "A", "C"],
        "bugs": {
            "xorou": {"correto": "chorou", "opcoes": ["chorou", "xorou", "xourou"]},
            "zacrifício": {"correto": "sacrifício", "opcoes": ["sacrifício", "zacrifício", "sacrifisio"]},
            "forca": {"correto": "força", "opcoes": ["força", "forca", "forsa"]},
            "poderoza": {"correto": "poderosa", "opcoes": ["poderosa", "poderoza", "poderoça"]}
        },
        "mec4_options": [
            ("Trocas de S por Z", True),
            ("Trocas de CH por X", False),
            ("Trocas de C por Ç", False),
            ("Trocas de G por J", False)
        ]
    },
    {
        "name": "Capítulo 2: Lenda do Mapinguari",
        "rank": "Explorador",
        "color": ACCENT_ORANGE,
        "paragraphs": [
            {"id": "A", "text": "A fera andava pesadamente pelas matas, devorando tudo o que encontrava. Os caçadores largavam a tigela de comida e evitavam a selva, com medo de encontrar a criatura selvajem."},
            {"id": "B", "text": "Dizem que o Mapinguari era um antigo índio guerreiro, majestoso e forte, que descobriu o segredo da imortalidade. Mas a magia teve um preço terrível."},
            {"id": "C", "text": "Hoje, quem se arrisca numa longa viajem pela mata densa sabe que não deve chingar a natureza. É preciso mexer com cuidado para não acordar o monstro."},
            {"id": "D", "text": "Ele se transformou num monstro enorme, coberto de pelos ruivos, com um olho só e uma boca assustadora na barriga, impossível não enchergar de longe."}
        ],
        "correct_order": ["B", "D", "A", "C"],
        "bugs": {
            "selvajem": {"correto": "selvagem", "opcoes": ["selvagem", "selvajem", "selvagên"]},
            "enchergar": {"correto": "enxergar", "opcoes": ["enxergar", "enchergar", "enxegar"]},
            "viajem": {"correto": "viagem", "opcoes": ["viagem", "viajem", "viagen"]},
            "chingar": {"correto": "xingar", "opcoes": ["xingar", "chingar", "ximgar"]}
        },
        "mec4_options": [
            ("Troca de G por J e X por CH", True),
            ("Troca de S por Z e C por Ç", False),
            ("Uso incorreto de H no início", False),
            ("Omissão de R no infinitivo", False)
        ]
    },
    {
        "name": "Capítulo 3: Lenda da Cobra Grande",
        "rank": "Guardião",
        "color": DANGER,
        "paragraphs": [
            {"id": "A", "text": "Com o passar do tempo, a cobra cresceu tanto que o rio ficou pequeno. Ela nadava pelo sentro do rio e se tornou a Boiúna, uma assonbração dos rios."},
            {"id": "B", "text": "Conta a lenda que uma mulher grávida deu à luz duas crianças gêmeas no nasimento mais estranho da aldeia. Uma delas tinha a forma de uma serpente escura e assustadora."},
            {"id": "C", "text": "A mãe, inosente, jogou a serpente no rio com medo. Lá, no silénsio da noite, ela se alimentava dos peixes e de qualquer animau que caísse na água."},
            {"id": "D", "text": "Os pescadores dizem que, com serteza, à noite, seus olhos brilham como fogo, e quando ela se move, um forte temporau e o som de tanbor anunciam sua chegada."},
            {"id": "E", "text": "A Iara, sereia dos rios, cantava uma música suave para atrair os pescadores. Ninguém resistia ao seu encanto na floresta."}
        ],
        "correct_order": ["B", "C", "A", "D"],
        "bugs": {
            "sentro": {"correto": "centro", "opcoes": ["centro", "sentro", "cêntro"]},
            "nasimento": {"correto": "nascimento", "opcoes": ["nascimento", "nasimento", "nacimento"]},
            "inosente": {"correto": "inocente", "opcoes": ["inocente", "inosente", "inossente"]},
            "silénsio": {"correto": "silêncio", "opcoes": ["silêncio", "silénsio", "cilêncio"]},
            "serteza": {"correto": "certeza", "opcoes": ["certeza", "serteza", "sertesa"]},
            "assonbração": {"correto": "assombração", "opcoes": ["assombração", "assonbração", "asombração"]},
            "animau": {"correto": "animal", "opcoes": ["animal", "animau", "animalo"]},
            "temporau": {"correto": "temporal", "opcoes": ["temporal", "temporau", "temporaw"]},
            "tanbor": {"correto": "tambor", "opcoes": ["tambor", "tanbor", "tâmbor"]}
        },
        "mec4_options": [
            ("Confusão entre C e S (ce/ci → se/si)", True),
            ("Uso de N antes de P/B e U no final", False),
            ("Troca de G por J e X por CH", False),
            ("Confusão entre SS e Ç", False)
        ]
    },
    {
        "name": "Capítulo 4: Lenda da Vitória-Régia",
        "rank": "Mestre",
        "color": GOLD,
        "paragraphs": [
            {"id": "A", "text": "Certa noite, Naiá viu o reflexo da lua nas águas escuras do lago. Pensando que a lua tinha descido para buscá-la, ela mergulhou com muita corassão."},
            {"id": "B", "text": "Naiá era uma jovem índia que se apaixonou por Jaci, a lua. Ela sonhava em ser transformada em uma estrela brilhante no céu, ao lado de Jaci."},
            {"id": "C", "text": "Jaci ficou com pena da belesa da jovem e a transformou não em uma estrela do céu, mas na Estrela das águas: a Vitória-Régia, que floresce à noite para encantar cada páçaro."},
            {"id": "D", "text": "Toda noite, ela corria pelas matas tentando alcançar a lua. A bela índia ficava triste quando não conseguia, sentindo uma enorme emossão."},
            {"id": "E", "text": "O boto cor-de-rosa surgia nas festas vestido de branco, dançando com as moças mais bonitas da aldeia."},
            {"id": "F", "text": "Nas noites de lua cheia, o lobisomem corria pelos campos assustando as ovelhas e os moradores da região."}
        ],
        "correct_order": ["B", "D", "A", "C"],
        "bugs": {
            "corassão": {"correto": "coração", "opcoes": ["coração", "corassão", "corasão"]},
            "belesa": {"correto": "beleza", "opcoes": ["beleza", "belesa", "beleça"]},
            "páçaro": {"correto": "pássaro", "opcoes": ["pássaro", "páçaro", "pácaro"]},
            "emossão": {"correto": "emoção", "opcoes": ["emoção", "emossão", "emosão"]}
        },
        "mec4_options": [
            ("Confusão entre SS, Ç e Z", True),
            ("Troca de C por S e H por NH", False),
            ("Uso incorreto de L no lugar de U", False),
            ("Omissão de M antes de P e B", False)
        ]
    }
]

WIDTH = 1280
HEIGHT = 720
