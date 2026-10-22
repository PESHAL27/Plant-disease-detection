"""
AgroScan AI - Verified Plant Disease Database
Maps 38 PlantVillage classes to detailed agricultural metadata, symptoms, and management guidelines.
Each class is paired with its authentic, crop-specific pathology and leaf imagery.
"""

DISEASE_DB = {
    "Apple Scab": {
        "crop": "Apple",
        "disease": "Apple Scab",
        "category": "Fungal Disease",
        "pathogen": "Venturia inaequalis",
        "severity": "Moderate to High",
        "description": "Apple scab produces dull olive-green to black velvety spots on leaves and fruit, causing premature leaf drop and deformed fruit.",
        "symptoms": "Olive-green to dark brown circular spots with velvety margins on upper leaf surfaces. Leaves may curl, turn yellow, and drop prematurely.",
        "management": "Apply preventive fungicides in early spring. Rake and destroy fallen leaves to reduce overwintering spore inocula. Ensure canopy airflow through pruning.",
        "image": "assets/apple_scab.jpg"
    },
    "Apple with Black Rot": {
        "crop": "Apple",
        "disease": "Black Rot (Frogeye Leaf Spot)",
        "category": "Fungal Disease",
        "pathogen": "Botryosphaeria obtusa",
        "severity": "High",
        "description": "Causes frogeye leaf spots on foliage, cankers on limbs, and firm brown rot that mummifies developing apples.",
        "symptoms": "Small purple specks expanding into circular lesions with tan centers and dark purple margins (frogeye appearance).",
        "management": "Prune out dead wood, cankers, and mummified fruit during dormant season. Apply captan or copper fungicides at petal fall.",
        "image": "assets/apple_black_rot.jpg"
    },
    "Cedar Apple Rust": {
        "crop": "Apple",
        "disease": "Cedar Apple Rust",
        "category": "Fungal Disease",
        "pathogen": "Gymnosporangium juniperi-virginianae",
        "severity": "Moderate",
        "description": "Heteroecious fungal disease requiring both juniper/cedar and apple trees to complete its life cycle.",
        "symptoms": "Bright yellow-orange or reddish spots on upper leaf surfaces. In mid-summer, tube-like fungal aecia emerge on the undersides.",
        "management": "Remove nearby eastern red cedar trees if practical. Plant resistant apple cultivars. Apply protective fungicides between pink bud and petal fall.",
        "image": "assets/cedar_apple_rust.jpg"
    },
    "Healthy Apple": {
        "crop": "Apple",
        "disease": "Healthy Foliage",
        "category": "Healthy Condition",
        "pathogen": "None",
        "severity": "None",
        "description": "The apple foliage exhibits uniform deep green coloration, intact leaf margins, and robust cellular structure without pathogen activity.",
        "symptoms": "Vibrant emerald green leaves, smooth surface, intact venation, and absence of necrotic spotting or powdery residue.",
        "management": "Maintain balanced nitrogen-potassium fertilization, regular scouting, and drip irrigation to preserve vigor.",
        "image": "assets/apple_healthy.jpg"
    },
    "Healthy Blueberry Plant": {
        "crop": "Blueberry",
        "disease": "Healthy Foliage",
        "category": "Healthy Condition",
        "pathogen": "None",
        "severity": "None",
        "description": "Vibrant, clean blueberry leaves indicating optimal soil acidity (pH 4.5-5.2) and nutrient availability.",
        "symptoms": "Lustrous dark green leaves with typical waxy cuticle and normal lanceolate shape.",
        "management": "Keep soil acidic with sulfur amendments and pine bark mulch. Maintain consistent root zone moisture.",
        "image": "assets/blueberry_healthy.jpg"
    },
    "Cherry with Powdery Mildew": {
        "crop": "Cherry",
        "disease": "Powdery Mildew",
        "category": "Fungal Disease",
        "pathogen": "Podosphaera clandestina",
        "severity": "Moderate",
        "description": "Fungal disease covering tender leaves and twigs with a superficial white powdery mycelial layer.",
        "symptoms": "White talcum-powder-like patches on leaves. Foliage may curl upward, distort, and drop prematurely.",
        "management": "Apply sulfur-based or myclobutanil fungicides when shoots are 2-4 inches long. Avoid excessive overhead irrigation.",
        "image": "assets/cherry_powdery_mildew.jpg"
    },
    "Healthy Cherry Plant": {
        "crop": "Cherry",
        "disease": "Healthy Foliage",
        "category": "Healthy Condition",
        "pathogen": "None",
        "severity": "None",
        "description": "Pristine cherry foliage showing healthy dark green leaf blades and vigorous shoot growth.",
        "symptoms": "Clean, unblemished ovate leaves with serrated margins and uniform chloroplast density.",
        "management": "Standard orchard maintenance, preventive copper sprays at bud break, and balanced N-P-K nutrition.",
        "image": "assets/cherry_healthy.jpg"
    },
    "Corn (Maize) with Cercospora and Gray Leaf Spot": {
        "crop": "Corn",
        "disease": "Gray Leaf Spot",
        "category": "Fungal Disease",
        "pathogen": "Cercospora zeae-maydis",
        "severity": "High",
        "description": "One of the most destructive corn foliar diseases, causing extensive photosynthetic tissue loss.",
        "symptoms": "Small tan spots that elongate into narrow rectangular lesions bounded by leaf veins. Lesions may coalesce.",
        "management": "Plant resistant hybrids. Practice crop rotation with non-host crops (soybean) and incorporate residue tillage.",
        "image": "assets/corn_gray_leaf_spot.jpg"
    },
    "Corn (Maize) with Common Rust": {
        "crop": "Corn",
        "disease": "Common Rust",
        "category": "Fungal Disease",
        "pathogen": "Puccinia sorghi",
        "severity": "Moderate",
        "description": "Fungal infection thriving in cool, humid weather, forming prominent rust-colored spore pustules.",
        "symptoms": "Small elongated cinnamon-brown pustules scattered across both upper and lower leaf surfaces.",
        "management": "Select resistant corn hybrids. Apply foliar triazole or strobilurin fungicides if pustules appear before silking.",
        "image": "assets/corn_common_rust.jpg"
    },
    "Corn (Maize) with Northern Leaf Blight": {
        "crop": "Corn",
        "disease": "Northern Corn Leaf Blight",
        "category": "Fungal Disease",
        "pathogen": "Setosphaeria turcica (Exserohilum turcicum)",
        "severity": "High",
        "description": "Causes large cigar-shaped necrotic lesions that can prematurely kill whole leaves during grain fill.",
        "symptoms": "Elliptical, grayish-green or tan lesions measuring 1 to 6 inches long with blunt ends.",
        "management": "Use resistant hybrids carrying Ht genes. Rotate crops and bury infected debris through conservation tillage.",
        "image": "assets/corn_northern_blight.jpg"
    },
    "Healthy Corn (Maize) Plant": {
        "crop": "Corn",
        "disease": "Healthy Foliage",
        "category": "Healthy Condition",
        "pathogen": "None",
        "severity": "None",
        "description": "Robust, deep-green corn leaves displaying uniform venation and vigorous vegetative development.",
        "symptoms": "Broad lanceolate leaves with strong central midribs, uniform green color, and absence of pustules or blights.",
        "management": "Maintain optimal nitrogen side-dressing and weed suppression during early canopy closure.",
        "image": "assets/corn_healthy.jpg"
    },
    "Grape with Black Rot": {
        "crop": "Grape",
        "disease": "Black Rot",
        "category": "Fungal Disease",
        "pathogen": "Guignardia bidwellii",
        "severity": "High",
        "description": "Destructive vineyard disease attacking leaves, shoots, and fruit clusters, shriveling berries into hard black mummies.",
        "symptoms": "Small circular reddish-brown leaf spots with distinct dark margins and tiny black pycnidia pimples.",
        "management": "Prune out infected mummies. Maintain canopy training for air circulation. Spray protectant fungicides (mancozeb).",
        "image": "assets/grape_black_rot.jpg"
    },
    "Grape with Esca (Black Measles)": {
        "crop": "Grape",
        "disease": "Esca (Black Measles)",
        "category": "Fungal Complex",
        "pathogen": "Phaeomoniella chlamydospora & Fomitiporia mediterranea",
        "severity": "High",
        "description": "Wood-decay trunk disease showing characteristic tiger-stripe foliar necrosis and dark berry spotting.",
        "symptoms": "Interveinal yellow and red discoloration forming distinctive 'tiger stripes' with necrotic margins.",
        "management": "Prune during dry periods. Treat pruning wounds with sealant. Remove and burn severely collapsed vines.",
        "image": "assets/grape_esca.jpg"
    },
    "Grape with Isariopsis Leaf Spot": {
        "crop": "Grape",
        "disease": "Isariopsis Leaf Spot",
        "category": "Fungal Disease",
        "pathogen": "Pseudocercospora vitis",
        "severity": "Moderate",
        "description": "Foliar disease common in warm, humid grape-growing zones causing premature defoliation.",
        "symptoms": "Dark brown, angular to irregular spots bounded by veins, often with a yellow halo.",
        "management": "Apply copper or sulfur sprays. Ensure open trellis canopies to facilitate rapid foliage drying.",
        "image": "assets/grape_leaf_spot.jpg"
    },
    "Healthy Grape Plant": {
        "crop": "Grape",
        "disease": "Healthy Foliage",
        "category": "Healthy Condition",
        "pathogen": "None",
        "severity": "None",
        "description": "Vigorous vine foliage supporting active photosynthesis and uniform berry cluster development.",
        "symptoms": "Crisp palmate leaves with vivid green pigmentation, intact margins, and healthy shoot tips.",
        "management": "Proper canopy shoot positioning, balanced potassium fertilization, and preventive mildew scouting.",
        "image": "assets/grape_healthy.jpg"
    },
    "Orange with Citrus Greening": {
        "crop": "Orange",
        "disease": "Citrus Greening (Huanglongbing)",
        "category": "Bacterial Disease",
        "pathogen": "Candidatus Liberibacter asiaticus (vectored by Asian citrus psyllid)",
        "severity": "Critical",
        "description": "A devastating, incurable phloem-limited bacterial disease that ruins citrus production worldwide.",
        "symptoms": "Asymmetrical blotchy mottle on leaves, yellowing of veins, and stunted, bitter, misshapen fruit.",
        "management": "Aggressive control of the insect vector (psyllids). Remove symptomatic infected trees to reduce reservoir.",
        "image": "assets/orange_citrus_greening.jpg"
    },
    "Peach with Bacterial Spot": {
        "crop": "Peach",
        "disease": "Bacterial Spot",
        "category": "Bacterial Disease",
        "pathogen": "Xanthomonas arboricola pv. pruni",
        "severity": "High",
        "description": "Bacterial disease causing shot-hole lesions on foliage and sunken pitting on peach fruit.",
        "symptoms": "Small water-soaked angular spots on leaves turning purple-black; centers drop out giving a shot-hole appearance.",
        "management": "Apply oxytetracycline or low-rate copper formulations during early growing season. Plant resistant peach varieties.",
        "image": "assets/peach_bacterial_spot.jpg"
    },
    "Healthy Peach Plant": {
        "crop": "Peach",
        "disease": "Healthy Foliage",
        "category": "Healthy Condition",
        "pathogen": "None",
        "severity": "None",
        "description": "Lush peach foliage with elongated lanceolate leaves free from bacterial or fungal pathogens.",
        "symptoms": "Bright glossy green leaves with serrated edges, uniform texture, and healthy apical extension.",
        "management": "Dormant copper sprays for leaf curl prevention, routine thinning, and summer drip irrigation.",
        "image": "assets/peach_healthy.jpg"
    },
    "Bell Pepper with Bacterial Spot": {
        "crop": "Pepper",
        "disease": "Bacterial Spot",
        "category": "Bacterial Disease",
        "pathogen": "Xanthomonas euvesicatoria",
        "severity": "High",
        "description": "Prevalent bacterial pathogen causing defoliation, blossom drop, and blistered fruit lesions in peppers.",
        "symptoms": "Small, water-soaked, circular to irregular dark spots on leaves with pale yellow haloes.",
        "management": "Use certified disease-free seeds. Avoid overhead irrigation. Apply copper bactericides mixed with mancozeb.",
        "image": "assets/pepper_bacterial_spot.jpg"
    },
    "Healthy Bell Pepper Plant": {
        "crop": "Pepper",
        "disease": "Healthy Foliage",
        "category": "Healthy Condition",
        "pathogen": "None",
        "severity": "None",
        "description": "Uniform, glossy bell pepper foliage reflecting balanced nitrogen and healthy root rhizosphere.",
        "symptoms": "Smooth ovate leaves with vibrant green coloration and sturdy stems free from blemishes.",
        "management": "Ensure calcium availability to avoid blossom end rot, mulching, and pest monitoring.",
        "image": "assets/pepper_healthy.jpg"
    },
    "Potato with Early Blight": {
        "crop": "Potato",
        "disease": "Early Blight",
        "category": "Fungal Disease",
        "pathogen": "Alternaria solani",
        "severity": "High",
        "description": "Common foliar fungal disease causing 'target board' lesions that defoliate potato canopies.",
        "symptoms": "Circular brown-black spots with concentric rings surrounded by a chlorotic yellow halo on older foliage.",
        "management": "Rotate crops every 2-3 years. Avoid leaf wetness. Apply protectant fungicides like chlorothalonil or mancozeb.",
        "image": "assets/potato_early_blight.jpg"
    },
    "Potato with Late Blight": {
        "crop": "Potato",
        "disease": "Late Blight",
        "category": "Oomycete / Water Mold",
        "pathogen": "Phytophthora infestans",
        "severity": "Critical",
        "description": "The notorious disease behind the Irish Potato Famine; rapidly destroys foliage and rots tubers.",
        "symptoms": "Large dark water-soaked lesions on leaves with white fuzzy sporulation visible on leaf undersides in high humidity.",
        "management": "Plant certified seed tubers. Apply systemic fungicides (metalaxyl/cymoxanil) immediately upon weather alerts.",
        "image": "assets/potato_late_blight.jpg"
    },
    "Healthy Potato Plant": {
        "crop": "Potato",
        "disease": "Healthy Foliage",
        "category": "Healthy Condition",
        "pathogen": "None",
        "severity": "None",
        "description": "Healthy potato canopy with compound leaves functioning efficiently for maximum tuber bulking.",
        "symptoms": "Crisp, pinnate green leaves with no lesions, necrotic margins, or wilt symptoms.",
        "management": "Proper hilling, steady moisture supply, and preventive scouting for Colorado potato beetle.",
        "image": "assets/potato_healthy.jpg"
    },
    "Healthy Raspberry Plant": {
        "crop": "Raspberry",
        "disease": "Healthy Foliage",
        "category": "Healthy Condition",
        "pathogen": "None",
        "severity": "None",
        "description": "Vibrant raspberry cane foliage with serrated leaflets and healthy cane development.",
        "symptoms": "Compound leaves with rich green upper surfaces and silvery-white hairy undersides.",
        "management": "Prune old floricanes post-harvest, trellis new primocanes, and ensure well-drained soils.",
        "image": "assets/raspberry_healthy.jpg"
    },
    "Healthy Soybean Plant": {
        "crop": "Soybean",
        "disease": "Healthy Foliage",
        "category": "Healthy Condition",
        "pathogen": "None",
        "severity": "None",
        "description": "Healthy trifoliate soybean leaves indicating robust nodulation and active nitrogen fixation.",
        "symptoms": "Pristine trifoliate leaflets with uniform green color, free from rust or cercospora lesions.",
        "management": "Maintain proper plant spacing, weed management, and monitor for soybean aphids.",
        "image": "assets/soybean_healthy.jpg"
    },
    "Squash with Powdery Mildew": {
        "crop": "Squash",
        "disease": "Powdery Mildew",
        "category": "Fungal Disease",
        "pathogen": "Podosphaera xanthii",
        "severity": "Moderate to High",
        "description": "Extremely prevalent cucurbit disease that impairs photosynthesis, causing premature leaf death and sunburned fruit.",
        "symptoms": "Circular white talcum-like powdery spots expanding across leaf blades and petioles.",
        "management": "Select resistant squash varieties. Apply potassium bicarbonate, horticultural oils, or sulfur fungicides.",
        "image": "assets/squash_powdery_mildew.jpg"
    },
    "Strawberry with Leaf Scorch": {
        "crop": "Strawberry",
        "disease": "Leaf Scorch",
        "category": "Fungal Disease",
        "pathogen": "Diplocarpon earlianum",
        "severity": "Moderate",
        "description": "Fungal disease causing widespread purplish spotting that dries leaves into a scorched appearance.",
        "symptoms": "Numerous small, irregular purple-to-dark-brown spots that lack clear white centers, causing leaf margins to curl up.",
        "management": "Remove old leaves after renovation. Use straw mulch to limit soil splashing. Apply captan or thiophanate-methyl.",
        "image": "assets/strawberry_leaf_scorch.jpg"
    },
    "Healthy Strawberry Plant": {
        "crop": "Strawberry",
        "disease": "Healthy Foliage",
        "category": "Healthy Condition",
        "pathogen": "None",
        "severity": "None",
        "description": "Lush trifoliate strawberry leaves showing strong root establishment and vibrant crown growth.",
        "symptoms": "Deep emerald trifoliate leaves with prominent serration and glossy leaf surfaces.",
        "management": "Clean drip irrigation, proper runner management, and clean straw mulching.",
        "image": "assets/strawberry_healthy.jpg"
    },
    "Tomato with Bacterial Spot": {
        "crop": "Tomato",
        "disease": "Bacterial Spot",
        "category": "Bacterial Disease",
        "pathogen": "Xanthomonas perforans / euvesicatoria",
        "severity": "High",
        "description": "Bacterial infection causing severe defoliation and blister-like lesions on tomato fruit.",
        "symptoms": "Small, dark, greasy or water-soaked lesions that turn black with a yellow halo. Center may drop out.",
        "management": "Use pathogen-free seeds. Avoid working in wet fields. Apply copper hydroxide paired with mancozeb.",
        "image": "assets/tomato_bacterial_spot.jpg"
    },
    "Tomato with Early Blight": {
        "crop": "Tomato",
        "disease": "Early Blight",
        "category": "Fungal Disease",
        "pathogen": "Alternaria solani",
        "severity": "High",
        "description": "This disease causes brown spots with concentric rings on older leaves and can reduce yield if not managed.",
        "symptoms": "Brown to black lesions with characteristic concentric rings ('target board' pattern) surrounded by chlorotic yellow halo.",
        "management": "Prune lower leaves to improve airflow. Mulch soil to prevent rain splash. Apply chlorothalonil, copper, or azoxystrobin fungicides.",
        "image": "assets/tomato_early_blight.jpg"
    },
    "Tomato with Late Blight": {
        "crop": "Tomato",
        "disease": "Late Blight",
        "category": "Oomycete / Water Mold",
        "pathogen": "Phytophthora infestans",
        "severity": "Critical",
        "description": "Highly aggressive pathogen that can defoliate entire tomato fields in wet, cool conditions within days.",
        "symptoms": "Large, dark, water-soaked lesions on leaves and stems, often with white fungal-like fuzz on undersides during humid mornings.",
        "management": "Destroy volunteer tomato/potato plants. Apply protective fungicides before rain events. Remove affected plants immediately.",
        "image": "assets/tomato_late_blight.jpg"
    },
    "Tomato with Leaf Mold": {
        "crop": "Tomato",
        "disease": "Leaf Mold",
        "category": "Fungal Disease",
        "pathogen": "Passalora fulva (Cladosporium fulvum)",
        "severity": "Moderate to High",
        "description": "Severe primarily in greenhouse and high-tunnel tomatoes where relative humidity exceeds 85%.",
        "symptoms": "Pale greenish-yellow spots on upper leaf surfaces matching olive-green to brown velvety fungal growth underneath.",
        "management": "Lower relative humidity below 85% with fans and venting. Space plants widely and apply copper or chlorothalonil.",
        "image": "assets/tomato_leaf_mold.jpg"
    },
    "Tomato with Septoria Leaf Spot": {
        "crop": "Tomato",
        "disease": "Septoria Leaf Spot",
        "category": "Fungal Disease",
        "pathogen": "Septoria lycopersici",
        "severity": "High",
        "description": "One of the most destructive foliage diseases of tomatoes, rapidly progressing from bottom leaves upward.",
        "symptoms": "Numerous small circular spots with dark brown margins and sunken grayish-white centers containing tiny black specks.",
        "management": "Rotate crops on a 3-year cycle. Water at the base via drip lines. Spray protectant fungicides at first symptom sign.",
        "image": "assets/tomato_septoria.jpg"
    },
    "Tomato with Spider Mites or Two-spotted Spider Mite": {
        "crop": "Tomato",
        "disease": "Spider Mite Damage",
        "category": "Pest Infestation",
        "pathogen": "Tetranychus urticae (Two-spotted spider mite)",
        "severity": "Moderate to High",
        "description": "Sap-sucking arachnids that feed on plant cells, creating yellow stippling and fine webbing.",
        "symptoms": "Fine yellow or white stippling on leaf surfaces, bronzing of foliage, and delicate webbing under leaves.",
        "management": "Introduce beneficial predatory mites (Phytoseiulus persimilis). Apply insecticidal soaps, neem oil, or selective miticides.",
        "image": "assets/tomato_spider_mites.jpg"
    },
    "Tomato with Target Spot": {
        "crop": "Tomato",
        "disease": "Target Spot",
        "category": "Fungal Disease",
        "pathogen": "Corynespora cassiicola",
        "severity": "High",
        "description": "Fungal pathogen producing concentric brown spots that can affect foliage, stems, and fruit.",
        "symptoms": "Pinpoint spots that enlarge into brown lesions with light brown centers and faint target-like concentric rings.",
        "management": "Ensure adequate plant spacing. Remove crop residues after harvest. Apply systemic fungicides.",
        "image": "assets/tomato_target_spot.jpg"
    },
    "Tomato Yellow Leaf Curl Virus": {
        "crop": "Tomato",
        "disease": "Yellow Leaf Curl Virus",
        "category": "Viral Disease",
        "pathogen": "Tomato yellow leaf curl virus (TYLCV), vectored by Bemisia tabaci (whitefly)",
        "severity": "Critical",
        "description": "Devastating viral disease spread by whiteflies causing extreme stunting and complete blossom abort.",
        "symptoms": "Upward curling and cupping of leaflet margins, pronounced interveinal yellowing, and severe plant stunting.",
        "management": "Control whitefly vectors using insect screens, reflective mulches, and systemic insecticides. Plant resistant hybrids.",
        "image": "assets/tomato_yellow_curl.jpg"
    },
    "Tomato Mosaic Virus": {
        "crop": "Tomato",
        "disease": "Mosaic Virus",
        "category": "Viral Disease",
        "pathogen": "Tomato mosaic virus (ToMV)",
        "severity": "High",
        "description": "Extremely stable virus spread mechanically by hands, tools, and infected debris, causing mosaic patterns.",
        "symptoms": "Mottled light and dark green patterns on leaves, puckering, distortion, and 'shoestring' leaf elongation.",
        "management": "Disinfect tools with trisodium phosphate. Wash hands before handling plants. Plant resistant varieties (Tm-2 gene).",
        "image": "assets/tomato_mosaic.jpg"
    },
    "Healthy Tomato Plant": {
        "crop": "Tomato",
        "disease": "Healthy Foliage",
        "category": "Healthy Condition",
        "pathogen": "None",
        "severity": "None",
        "description": "Vibrant, pest-free tomato canopy with robust compound leaves and active vegetative or reproductive growth.",
        "symptoms": "Deep green serrated leaflets, strong turgidity, clean stems, and zero necrotic spotting or viral curling.",
        "management": "Maintain consistent drip irrigation, cage/stake vines, and provide calcium nitrate feeding.",
        "image": "assets/tomato_healthy.jpg"
    }
}

# Order of 38 classes matching PlantVillage alphabetical standard and model_v1.pt class_to_idx.json
RAW_TO_FRIENDLY_MAP = {
    "Apple___Apple_scab": "Apple Scab",
    "Apple___Black_rot": "Apple with Black Rot",
    "Apple___Cedar_apple_rust": "Cedar Apple Rust",
    "Apple___healthy": "Healthy Apple",
    "Blueberry___healthy": "Healthy Blueberry Plant",
    "Cherry_(including_sour)___Powdery_mildew": "Cherry with Powdery Mildew",
    "Cherry_(including_sour)___healthy": "Healthy Cherry Plant",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": "Corn (Maize) with Cercospora and Gray Leaf Spot",
    "Corn_(maize)___Common_rust_": "Corn (Maize) with Common Rust",
    "Corn_(maize)___Northern_Leaf_Blight": "Corn (Maize) with Northern Leaf Blight",
    "Corn_(maize)___healthy": "Healthy Corn (Maize) Plant",
    "Grape___Black_rot": "Grape with Black Rot",
    "Grape___Esca_(Black_Measles)": "Grape with Esca (Black Measles)",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": "Grape with Isariopsis Leaf Spot",
    "Grape___healthy": "Healthy Grape Plant",
    "Orange___Haunglongbing_(Citrus_greening)": "Orange with Citrus Greening",
    "Peach___Bacterial_spot": "Peach with Bacterial Spot",
    "Peach___healthy": "Healthy Peach Plant",
    "Pepper,_bell___Bacterial_spot": "Bell Pepper with Bacterial Spot",
    "Pepper,_bell___healthy": "Healthy Bell Pepper Plant",
    "Potato___Early_blight": "Potato with Early Blight",
    "Potato___Late_blight": "Potato with Late Blight",
    "Potato___healthy": "Healthy Potato Plant",
    "Raspberry___healthy": "Healthy Raspberry Plant",
    "Soybean___healthy": "Healthy Soybean Plant",
    "Squash___Powdery_mildew": "Squash with Powdery Mildew",
    "Strawberry___Leaf_scorch": "Strawberry with Leaf Scorch",
    "Strawberry___healthy": "Healthy Strawberry Plant",
    "Tomato___Bacterial_spot": "Tomato with Bacterial Spot",
    "Tomato___Early_blight": "Tomato with Early Blight",
    "Tomato___Late_blight": "Tomato with Late Blight",
    "Tomato___Leaf_Mold": "Tomato with Leaf Mold",
    "Tomato___Septoria_leaf_spot": "Tomato with Septoria Leaf Spot",
    "Tomato___Spider_mites Two-spotted_spider_mite": "Tomato with Spider Mites or Two-spotted Spider Mite",
    "Tomato___Target_Spot": "Tomato with Target Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": "Tomato Yellow Leaf Curl Virus",
    "Tomato___Tomato_mosaic_virus": "Tomato Mosaic Virus",
    "Tomato___healthy": "Healthy Tomato Plant"
}

ORDERED_DB_KEYS = list(DISEASE_DB.keys())

def get_disease_info(identifier) -> dict:
    """
    Returns metadata for a given class label, raw folder name, or numeric index.
    Always returns a dictionary with full biological context.
    """
    # 1. Numeric index
    if isinstance(identifier, int):
        if 0 <= identifier < len(ORDERED_DB_KEYS):
            key = ORDERED_DB_KEYS[identifier]
            res = dict(DISEASE_DB[key])
            res["friendly_name"] = key
            return res
        identifier = str(identifier)
    
    # 2. Raw PlantVillage class name (e.g., 'Tomato___Early_blight')
    if identifier in RAW_TO_FRIENDLY_MAP:
        friendly = RAW_TO_FRIENDLY_MAP[identifier]
        res = dict(DISEASE_DB[friendly])
        res["friendly_name"] = friendly
        res["raw_class_label"] = identifier
        return res
        
    # 3. Direct match in DISEASE_DB
    if identifier in DISEASE_DB:
        res = dict(DISEASE_DB[identifier])
        res["friendly_name"] = identifier
        return res
    
    # 4. Fuzzy match
    ident_str = str(identifier).lower().replace("_", " ").replace("-", " ")
    for key, data in DISEASE_DB.items():
        k_clean = key.lower().replace("_", " ").replace("-", " ")
        if ident_str in k_clean or k_clean in ident_str:
            res = dict(data)
            res["friendly_name"] = key
            return res
            
    # Default fallback
    return {
        "crop": "General Plant",
        "disease": str(identifier),
        "friendly_name": str(identifier),
        "category": "Detected Condition",
        "pathogen": "Identified Plant Condition",
        "severity": "Standard",
        "description": f"Classification result returned by the model: {identifier}.",
        "symptoms": "Visual patterns on the leaf matched this disease class.",
        "management": "Isolate symptomatic plants, maintain adequate canopy airflow, and consult local agronomy specialists.",
        "image": "assets/healthy_leaf.jpg"
    }

def get_all_crops() -> list:
    """Returns sorted unique list of crops."""
    crops = set()
    for item in DISEASE_DB.values():
        crops.add(item["crop"])
    return sorted(list(crops))

