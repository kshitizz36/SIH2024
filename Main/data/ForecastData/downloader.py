import requests
import concurrent.futures

base_url = "https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl"
dir_param = "%2Fgfs.20240902%2F18%2Fatmos"
file_prefix = "gfs.t18z.pgrb2.0p25.anl"

var_VFLX = "on"
var_VIS = "on"
lev_surface = "on"

toplat = "31.1859"
leftlon = "20.0026"
rightlon = "146.8982"
bottomlat = "-60.0"

def download_file(hour):
    hour_str = f"f{hour:03d}"

    full_url = (
        f"{base_url}?dir={dir_param}&file={file_prefix}&"
        f"var_VFLX={var_VFLX}&var_VIS={var_VIS}&lev_surface={lev_surface}&"
        f"toplat={toplat}&leftlon={leftlon}&rightlon={rightlon}&bottomlat={bottomlat}"
    )

    try:
        response = requests.get(full_url)
    except Exception as e:
        print(f"Error downloading {full_url}: {e}")
        return None


    filename = f"tmp/gfs_{hour_str}.grb2"
    with open(filename, "wb") as f:
        f.write(response.content)

    print(f"Downloaded and saved {filename}")
    return filename

with concurrent.futures.ThreadPoolExecutor() as executor:
    hours = range(0, 385, 1)
    
    futures = {executor.submit(download_file, hour): hour for hour in hours}

   
    for future in concurrent.futures.as_completed(futures):
        hour = futures[future]
        try:
            result = future.result()
        except Exception as exc:
            print(f"Hour {hour} generated an exception: {exc}")
        else:
            if result:
                print(f"Hour {hour} file downloaded: {result}")

print("All files downloaded successfully.")
