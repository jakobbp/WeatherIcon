# WeatherIcon
Bottle RS that returns current weather estimation, based on CumulusMX logs.

## About
ReST service, running on a built-in HTTP server, that serves current weather representation images.
Returned image is determined by the ratio of measured solar radiation and theoretical maximum solar radiation at the time and geographical loaction. Solar radiation values are extracted from [CumulusMX](https://cumuluswiki.wxforum.net/a/Cumulus_MX) [monthly log files](https://cumuluswiki.wxforum.net/a/Monthly_log_files).

## Requirements
 - [Bottle](https://bottlepy.org/docs/dev/)

## Usage
Running the following will start a lightweight HTTP server on port 8000:
```bash
python weathericon.py
```

This exposes the following two ReST methods:

 - `http://[host]:8000/current` - returns the weather representation image based on the single latest solar radiation measurement and
 - `http://[host]:8000/average` - returns the weather representation image based on the average of the latest five solar radiation measurements.
