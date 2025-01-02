CREATE TABLE "hourly_weather_data" (
  "id" varchar(20) PRIMARY KEY,
  "date_id" varchar(10),
  "time_id" varchar(10),
  "location_id" varchar(10),
  "temperature_2m" numeric,
  "relative_humidity_2m" numeric,
  "dew_point_2m" numeric,
  "apparent_temperature" numeric,
  "precipitation_probability" numeric,
  "precipitation" numeric,
  "rain" numeric,
  "showers" numeric,
  "weather_code" varchar(10),
  "pressure_msl" numeric,
  "surface_pressure" numeric,
  "cloud_cover" numeric,
  "visibility" numeric,
  "evapotranspiration" numeric,
  "vapour_pressure_deficit" numeric,
  "wind_speed_10m" numeric,
  "wind_direction_10m" numeric,
  "wind_gusts_10m" numeric,
  "uv_index" numeric,
  "uv_index_clear_sky" numeric,
  "is_day" varchar(10),
  "sunshine_duration" numeric
);

CREATE TABLE "weather_code" (
  "id" varchar(10) PRIMARY KEY,
  "name" varchar(50)
);

CREATE TABLE "times_of_day" (
  "id" varchar(10) PRIMARY KEY,
  "name" varchar(20)
);

CREATE TABLE "dim_date" (
  "id" varchar(10) PRIMARY KEY,
  "date" date,
  "year" int,
  "quarter" int,
  "month" int,
  "day" int
);

CREATE TABLE "dim_time" (
  "id" varchar(10) PRIMARY KEY,
  "time" time,
  "hour" int
);

CREATE TABLE "hourly_aq_data" (
  "id" varchar(20) PRIMARY KEY,
  "date_id" varchar(10),
  "time_id" varchar(10),
  "location_id" varchar(10),
  "pm10" numeric,
  "pm2_5" numeric,
  "carbon_monoxide" numeric,
  "carbon_dioxide" numeric,
  "nitrogen_dioxide" numeric,
  "sulphur_dioxide" numeric,
  "ozone" numeric,
  "methane" numeric,
  "aerosol_optical_depth" numeric,
  "dust" numeric
);

CREATE TABLE "dim_location" (
  "id" varchar(10) PRIMARY KEY,
  "lat" numeric,
  "lon" numeric,
  "name" varchar(50)
);

ALTER TABLE "hourly_weather_data" ADD FOREIGN KEY ("weather_code") REFERENCES "weather_code" ("id");

ALTER TABLE "hourly_weather_data" ADD FOREIGN KEY ("is_day") REFERENCES "times_of_day" ("id");

ALTER TABLE "hourly_weather_data" ADD FOREIGN KEY ("date_id") REFERENCES "dim_date" ("id");

ALTER TABLE "hourly_aq_data" ADD FOREIGN KEY ("date_id") REFERENCES "dim_date" ("id");

ALTER TABLE "hourly_weather_data" ADD FOREIGN KEY ("time_id") REFERENCES "dim_time" ("id");

ALTER TABLE "hourly_aq_data" ADD FOREIGN KEY ("time_id") REFERENCES "dim_time" ("id");

ALTER TABLE "hourly_aq_data" ADD FOREIGN KEY ("location_id") REFERENCES "dim_location" ("id");

ALTER TABLE "hourly_weather_data" ADD FOREIGN KEY ("location_id") REFERENCES "dim_location" ("id");
