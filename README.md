# vector-tile-projection-test
Some vector tiles in various projections to test maputnik openlayers projection support

[![stability-experimental](https://img.shields.io/badge/stability-experimental-orange.svg)][stability]

[stability]:   https://github.com/orangemug/stability-badges#experimental



## Usage
Just run

```
docker-compose run dev sh -c "rm -rf vectortiles/*; python3 mvtbot.py definition.json"
docker-compose up
```

There are some styles you can try out in the [experimental projection Maputnik branch](https://github.com/maputnik/editor/compare/master...orangemug:feature/ol-projections)

 - Local - points to tiles hosted at (`http://localhost:5007`)
   - <http://localhost:5007/styles/epsg102003.json>
   - <http://localhost:5007/styles/epsg3031.json>
 - Hosted (links load in Maputnik)
   - [https://orangemug.github.io/vector-tiles-projection-test/styles/epsg102003.json](https://1397-84182601-gh.circle-artifacts.com/0/artifacts/build/index.html#0.34/0/0?style=https://orangemug.github.io/vector-tiles-projection-test/styles/epsg102003.json)
   - [https://orangemug.github.io/vector-tiles-projection-test/styles/epsg3031.json](https://1397-84182601-gh.circle-artifacts.com/0/artifacts/build/index.html#0.34/0/0?style=https://orangemug.github.io/vector-tiles-projection-test/styles/epsg3031.json)


## License
MIT

