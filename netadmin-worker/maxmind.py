import sys, requests, zipfile, csv, json
from pathlib import Path
from datetime import datetime, timezone

class MaxMind():
    download_key_file="./maxmind/conf.json"
    download_key=None
    download_file_suffix='zip'
    timestamp=datetime.now(timezone.utc).strftime('%Y%m%d')

    def importDownloadKey(self):
        file=Path(self.download_key_file)

        if not file.exists():
            return False

        jconfig=open(file)
        data=json.load(jconfig)

        self.download_key=data["download_key"]

        return True

    def makeDir(self, path):
        db_dir=Path(path)
        if not db_dir.exists():
            db_dir.mkdir(parents=True)

        return db_dir

    def getDatabaseTree(self, source):
        db_dirs=[x for x in source.iterdir() if x.is_dir()]
        return db_dirs

    def autodiscoveryCsvDB(self, db_dir,db_file='GeoLite2-Country-Locations-en.csv'):
        geoip_db_dir=self.getDatabaseTree(db_dir)
        geoip_db_file=Path("{}/{}".format(geoip_db_dir[0],db_file))

        if not geoip_db_file.exists():
                return False

        return geoip_db_file

    def downloadCsvDB(self, download_file_name, tmp_dir, extract_dir):
        self.importDownloadKey()
        download_file_path=tmp_dir / download_file_name
        download_file_url='https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-Country-CSV&license_key={}&suffix={}'.format(self.download_key,self.download_file_suffix)

        response=requests.get(download_file_url)

        if not response.status_code == 200:
                return False

        if not download_file_path.write_bytes(response.content):
                return False

        with zipfile.ZipFile(download_file_path) as z:
            for file in z.namelist():
                if 'GeoLite2-Country-Blocks-IPv4.csv' in file:
                    z.extract(file, extract_dir)
                if 'GeoLite2-Country-Locations-en.csv' in file:
                    z.extract(file, extract_dir)

        return True

    def downloadDB(self):
        download_file_name=Path('file.{}'.format(self.download_file_suffix))

        tmp_dir=self.makeDir('./maxmind/tmp')
        db_dir=self.makeDir('./maxmind/database')
        extract_db_dir=self.makeDir('./maxmind/database/{}'.format(self.timestamp))

        self.downloadCsvDB(download_file_name,tmp_dir, extract_db_dir)

        return True
