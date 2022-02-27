import json
from OpenLightControlGui.fixture_model import Manufacturer, Fixture

def get_fixtures(ofl: str) -> 'dict[str, dict[str, Fixture]]':
    import os
    import json
    with open(ofl+"manufacturers.json") as f:
        mans: 'dict[str, Manufacturer]' = {key: Manufacturer(key, val) for key, val in json.load(f).items() if not "$" in key}
    fixturesByManu: 'dict[str, dict[str, Fixture]]' = {}
    for key, man in mans.items():
        lis = os.listdir(ofl+key)
        fixturesByManu[key] = {}
        for fix in lis:
            with open(ofl+key+"/"+fix) as f:
                temp = Fixture(man, fix[:-5], json.load(f))
            fixturesByManu[key][fix[:-5]] = temp
    
    return fixturesByManu
