import sys, requests, zipfile
from pathlib import Path
from datetime import datetime, timezone

class MaxMind():
    download_key="00000000"
    timestamp=datetime.now(timezone.utc).strftime('%Y%m%d')
    root_dir="./maxmind"
    tmp_dir="./maxmind/tmp"
    db_dir="./maxmind/database"
    download_file_extension='zip'
    gl2_country_blocks_ipv4='GeoLite2-Country-Blocks-IPv4.csv'
    gl2_country_location_en='GeoLite2-Country-Locations-en.csv'
    last_error=""

    def makeDir(self, path):
        dir=Path(path)

        if not dir.exists():
            dir.mkdir(parents=True)

        return dir

    def autodiscoveryCsvDB(self, db_dir, db_file):
        try:
            geoip_db_dir=[x for x in db_dir.iterdir() if x.is_dir()]
            geoip_db_file=Path("{}/{}".format(geoip_db_dir[0],db_file))

            if not geoip_db_file.exists():
                return False

        except IndexError:
            return False

        return geoip_db_file

    def getCsvDB(self):
        self.makeDir(self.root_dir)
        tmp_dir=self.makeDir(self.tmp_dir)
        db_dir=self.makeDir(self.db_dir)
        extract_db_dir=self.makeDir("{}/{}".format(db_dir, self.timestamp))

        if not self.autodiscoveryCsvDB(extract_db_dir, self.gl2_country_blocks_ipv4):
            download_file_name=Path('file.{}'.format(self.download_file_extension))
            download_file_path=tmp_dir / download_file_name
            download_file_url='https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-Country-CSV&license_key={}&suffix={}'.format(self.download_key,self.download_file_extension)

            response=requests.get(download_file_url)

            if not response.status_code == 200:
                self.last_error="Download error - Check your download key"
                return False

            if not download_file_path.write_bytes(response.content):
                self.last_error="Error saving data"
                return False

            with zipfile.ZipFile(download_file_path) as z:
                for file in z.namelist():
                    if self.gl2_country_blocks_ipv4 in file:
                        z.extract(file, extract_db_dir)
                    if self.gl2_country_location_en in file:
                        z.extract(file, extract_db_dir)

        self.gl2_country_blocks_ipv4_db = self.autodiscoveryCsvDB(extract_db_dir, self.gl2_country_blocks_ipv4)
        self.gl2_country_location_en_db = self.autodiscoveryCsvDB(extract_db_dir, self.gl2_country_location_en)

        return True
