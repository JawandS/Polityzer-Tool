import json
import os
import time
import tldextract
from virustotal_python import Virustotal
from base64 import urlsafe_b64encode

# get virustotal api key
API_KEY = os.environ.get("VIRUSTOTAL_API_KEY")

# set delay
DELAY = 30 # seconds

# set up virustotal instance
vtotal = Virustotal(API_KEY=API_KEY, API_VERSION="v3")

# gather all outbound and site links
all_candidates = set()
with open('../../active_html/results/link_extractor_result.json', 'r') as f:
    data = json.load(f)
    # go through links
    for candidate in data:
        # add website
        all_candidates.add(candidate)

# valid candidtes
# valid_candidates = ['GearyMHiggins', 'JackieHopeGlass', 'DucMTruong', 'LukeETorian', 'NicholasSOlenik', 'NhanCHuynh', 'KannanSrinivasan', 'DanIHelmer', 'KathyKLTran', 'SaraHRatcliffe', 'AmandaEBatten', 'AlfonsoHLopez', 'JohnQSmith', 'RobertDBobbyOrrockSr', 'MichaelCKarslake', 'MichaelACherry', 'CarrieEmersonCoyner', 'KarenLJenkins', 'JeremyDRodden', 'TerryGKilgore', 'EricRZehr', 'JamesAThomasJr', 'KristinLHoffman', 'NadariusEClark', 'KarenAKeys-Gamarra', 'PatrickAHope', 'RichardCRipSullivanJr', 'MarkDSickles', 'JoshEThomas', 'RaeCCousins', 'DeloresLMcQuinn', 'RLeeWareJr', 'AlexQAskew', 'MadelynMadyRodriguez', 'MarciaSCiaPrice', 'RodneyTWillett', 'MarkLEarleyJr', 'SSamRasoul', 'HOttoWachsmannJr', 'PaulEKrizek', 'JohnSitkaIII', 'TravisSNembhard', 'AmyJLaufer', 'DestinyLLevereBolling', 'DavidLOwen', 'CToddGilbert', 'AnneFerrellTata', 'StephenCMiller-PittsJr', 'JohnTStirrup', 'WilliamDBillWiley', 'PhilMHernandez', 'VivianEWatts', 'AtoosaRReaser', 'JoshuaGCole', 'MarkJLux', 'NickJFreitas', 'JChristianChrisObenshain', 'BetsyBCarr', 'LesRAdams', 'WChadGreen', 'ElizabethBBennett-Parker', 'BrianaDSewell', 'JosephPJoeMcNamara', 'EdwardFMcGovern', 'WendellSWalker', 'ACCordoza', 'RobertSBloxomJr', 'AdeleYMcClure', 'PatriciaLynnQuesenberry', 'WilliamPDavis', 'DeloresROates', 'SteveDHarvey', 'DaveACranceJr', 'MaxBFisher', 'EllenHCampbell', 'KimATaylor', 'CatAPorterfield', 'LeonardBLacey', 'LRileyShaia', 'JamesAJayLeftwichJr', 'LeePetersIII', 'RobertLRobBanseJr', 'MichaelJDillender', 'MattJWaters', 'JeionAWard', 'PhillipAPhilScott', 'DonLScottJr', 'DavidLBulova', 'ScottAWyatt', 'MarcusBSimon', 'AndrewBAndyPittman', 'IreneShin', 'KatrinaECallsen', 'JasonSBallard', 'IanTravisLovejoy', 'CECliffHayesJr', 'JamesVTully', 'KarenSGreenhalgh', 'RoziaAJRHensonJr', 'DebraDGardner', 'LarryJJackson', 'HFBuddyFowlerJr', 'HillaryPughKent', 'KarrieKDelaney', 'WrenMWilliams', 'HollyMSeibold', 'RachelALevy', 'MichaelBFeggans', 'ChrisSRunion', 'JenniferKWoofter', 'MichaelJWebert', 'CharnieleLHerring', 'FernandoJMartyMartinez', 'LillianVFranklin', 'TerryLAustin', 'KimberlyPopeAdams', 'JasonAFord', 'DeborahIRenieGates', 'FrankMRuffJr', 'JenniferDCarrollFoy', 'WilliamMBillStanleyJr', 'MamieELocke', 'GregoryJMoulthrop', 'RussetWPerry', 'LLouiseLucas', 'NatanDMcKenzie', 'EmilyGScott', 'WilliamRBillDeSteph', 'LamontBagby', 'SaddamAzlanSalim', 'JenniferBBoysko', 'TTravisHackworth', 'SchuylerTVanValkenburg', 'RichardHStuart', 'DavidAHenshaw', 'JohnJMcGuireIII', 'PATrishWhite-Boyd', 'KennethDKenReid', 'BryceEReeves', 'GlenHSturtevantJr', 'DouglassHaydenFisher', 'LashrecseDAird', 'AaronRRouse', 'RCreighDeeds', 'ChristieNewCraig', 'ToddEPillion', 'JDDannyDiggs', 'BarbaraAFavola', 'PhilipAHamilton', 'AdamPEbbin', 'JoliciaAWard', 'EricFDitri', 'RobertWBeckman', 'TimmyFFrench', 'DavidWMarsden', 'JoshuaJHuffman', 'JulieAnnaPerry', 'MarkDObenshain', 'TaraADurant', 'StellaGPekarsky']
# get outbound links
outbound_links = set()
candidate_mapping  = {}
for candidate in all_candidates:
    # check if valid candidate
    # if candidate not in valid_candidates:
        # print(f"Skipping {candidate} as not a valid candidate.")
        # continue
    # get candidate data
    office = data[candidate]['office']
    website = f"{tldextract.extract(data[candidate]['website']).domain}.{tldextract.extract(data[candidate]['website']).suffix}".lower()
    # add to mapping
    candidate_mapping[candidate] = [office, website]
    outbound_links.add(website)

    for link in data[candidate]['outbound_links']:
        # extract domain
        domain = f"{tldextract.extract(link).domain}.{tldextract.extract(link).suffix}".lower()
        # add to lists
        outbound_links.add(domain)
        candidate_mapping[candidate].append(domain)

# remove links already downloaded
already_done = set()
for filename in os.listdir("virustotal_results"):
    if filename.endswith(".txt"):
        already_done.add(filename[:-4])
# remove links that have 404 error
with open("virustotal_error.log", "r") as f:
    for line in f:
        link = line.split("\t")[0]
        err_msg = line.split("\t")[1]
        if "429" not in err_msg: # not quota exceeded error
            already_done.add(link)
for link in already_done:
    outbound_links.remove(link)
print(f"Total number of links: {len(outbound_links)}")


# use virustotal
error_file = open("virustotal_error.log", "a")
for link in outbound_links:
    print("working on ", link)
    try:
        # sending scan request to virustotal
        response = vtotal.request("urls", data={"url": link}, method="POST")
        url_id = urlsafe_b64encode(link.encode()).decode().strip("=")
        # getting analysis response from virustotal
        analysis_resp = vtotal.request(f"urls/{url_id}")
        response_data = analysis_resp.data
        # write results
        with open(f"virustotal_results/{link}.txt", "w") as f:
            json.dump(response_data, f, indent=2)
        time.sleep(DELAY)
    except Exception as err:
        print(f"An error occurred: {err}\nCatching and continuing with program.")
        error_file.write(link + "\t" + str(err) + "\n")
        if "429" in str(err):
            print("quota exceeded")
            break
        time.sleep(DELAY)

# write mapping
with open('virustotal_mapping.json', 'w') as f:
    json.dump(candidate_mapping, f, indent=2)