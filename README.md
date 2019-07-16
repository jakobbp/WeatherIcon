# WeatherIcon
Bottle RS that returns current weather estimation, based on CumulusMX logs.

## About
ReST service, running on a built-in HTTP server, that serves current weather representation images.
Returned image is determined by the ratio of measured solar radiation and theoretical maximum solar radiation at the time and geographical location. Solar radiation values are extracted from [CumulusMX](https://cumuluswiki.wxforum.net/a/Cumulus_MX) [monthly log files](https://cumuluswiki.wxforum.net/a/Monthly_log_files).

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

## Customization
Behaviour, calculations and results of the service can be customized through the attached JSON and image files.

`wi_settings.json` contains general settings:

 - `host`: [Server address to bind to](https://bottlepy.org/docs/dev/_modules/bottle.html#run). Use `0.0.0.0` to listens on all interfaces including the external one.
 - `port`: [Server port to bind to](https://bottlepy.org/docs/dev/_modules/bottle.html#run). Values below 1024 require root privileges.
 - `dataSource`: URL to a [CumulusMX monthly log file](https://cumuluswiki.wxforum.net/a/Monthly_log_files) to parse the solar radiation data from.
 - `averageSamples`: The number of last log data entries to use when calculating the average solar radiation.

`radiation_threshold_images.json` contains mapping between image resources solar radiation ratio values.
```bash
{
  "[ratio]": "[relative resource path]",
  ...
}
```
_Ratio_ is calculated by dividing measured solar radiation with the theoretical maximal solar radiation at the measurement time. This _ratio threshold_ is then used as the _inclusive upper bound value_ when determining which image to return (meaning, that the corresponding image will be returned when the ratio is less or equal to this value and greater than the next defined ratio threshold).

Threshold to image mapping supports any number of mapping entries, but the threshold ratios should be non-negative and unique values, otherwise unexpected behaviour may occur.
