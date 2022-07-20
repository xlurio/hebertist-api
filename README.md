# HebertistAPI

Welcome to the Hebertist REST API! This API was made with the propose of making easier to us, mere peasants, to buy games with lower prices by comparing the price of a variety of games in multiple stores. Here are some of the features already running:
- Retrieve the rank of lowest prices from the `N`th to the `K`th to the element in the database;
- Filter best prices by the name of the game;
- Filter prices by game ID to compare prices between stores;
- Update game prices every three days;
- Update list of games every month;


## Summary

- [Retrieve Prices](#retrieve-prices)
  - [Filter Prices By Game ID](#filter-prices-by-game-id)

- [Retrieve The Best Prices Only](#retrieve-the-best-prices-only)
  - [Retrieve Best Price](#retrieve-best-price)
  - [Filter Best Prices By Game Name](#filter-best-prices-by-game-name)

- [Running Locally](#running-locally)
  - [Requirements](#requirements)
  - [Downloading](#downloading)
  - [Running](#running)
  - [Making Requests](#making-requests)


## Retrieve Prices

One of the most basic requests you can make in Herbertist REST API is retrieving all prices stored in its database. To achieve it, all you need to do is make a request the `/api/game/prices/` endpoint and you should get a response similar to this one:

```
{
  "count": 193,
  "next": "http://localhost:8000/api/game/prices/?page=2",
  "previous": null,
  "results": [
    {
      "id": 64,
      "game": 1246,
      "store": 3,
      "price": "1.29",
      "link": "https://www.gog.com/en/game/zombie_night_terror"
    },
    {
      "id": 71,
      "game": 1248,
      "store": 1,
      "price": "1.95",
      "link": "https://www.greenmangaming.com/games/waveform/"
    },
    {
      "id": 180,
      "game": 1248,
      "store": 2,
      "price": "1.95",
      "link": "https://store.steampowered.com/app/204180/Waveform/?snr=1_7_7_151_150_1"
    },
    {
      "id": 32,
      "game": 82,
      "store": 3,
      "price": "2.49",
      "link": "https://www.gog.com/en/game/splinter_cell"
    }
  ]
}
```

For performance purposes, this endpoint is paged. To navigate between pages, you can use the parameter `page` like this: `/api/game/prices/?page=[n]`, where `[n]` is the page number you desire.


### Filter Prices By Game ID

To compare the prices of a game between stores (which is the main purpose of why this endpoint was created) you can use the parameter `game_id`
like this: `/api/game/prices/?game_id=[n]` where `[n]` is the ID number of the desired game. 

`GET /api/game/prices/?game_id=1246`

```

{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 64,
            "game": 1246,
            "store": 3,
            "price": "1.29",
            "link": "https://www.gog.com/en/game/zombie_night_terror"
        },
        {
            "id": 62,
            "game": 1246,
            "store": 1,
            "price": "2.60",
            "link": "https://www.greenmangaming.com/games/zombie-night-terror/"
        },
        {
            "id": 141,
            "game": 1246,
            "store": 2,
            "price": "25.99",
            "link": "https://store.steampowered.com/app/416680/Zombie_Night_Terror/?snr=1_7_7_151_150_1"
        }
    ]
}
```

P.S.: If you don't know the ID of the game you desire, check the game name filter on the best [prices](#filter-best-prices-by-game-name) endpoint.


## Retrieve The Best Prices Only

If in opposite to compare prices, all you want is to get the best price you can access the `/api/game/prices/best_prices` endpoint:

```
[
  {
    "id": 71,
    "game": {
    "id": 1248,
    "name": "Waveform",
    "score": 81
  },
    "store": {
    "id": 1,
    "name": "Greenman Gaming",
    "link": null
  },
    "price": "1.95",
    "link": "https://www.greenmangaming.com/games/waveform/"
  }
]
```

By just requesting it how it is, it will only return the **one** best price of all games and stores. To effectivelly use this endpoint, you can use its parameters like the `from` and `to`, which allows you to filter, respectivelly, the lower and upper bounds of the best prices ranking. For example, the result of requesting `/api/game/prices/best_prices/?to=3` will be a response with the three best prices of individual games in the database:

```
[
  {
    "id": 71,
    "game": {
      "id": 1248,
      "name": "Waveform",
      "score": 81
    },
    "store": {
      "id": 1,
      "name": "Greenman Gaming",
      "link": null
    },
    "price": "1.95",
    "link": "https://www.greenmangaming.com/games/waveform/"
  },
  {
    "id": 62,
    "game": {
      "id": 1246,
      "name": "Zombie Night Terror",
      "score": 81
    },
    "store": {
      "id": 1,
      "name": "Greenman Gaming",
      "link": null
    },
    "price": "2.60",
    "link": "https://www.greenmangaming.com/games/zombie-night-terror/"
  },
  {
    "id": 73,
    "game": {
      "id": 134,
      "name": "Brothers: A Tale of Two Sons",
      "score": 79
  },
    "store": {
      "id": 3,
      "name": "GOG.com",
      "link": null
    },
    "price": "2.99",
    "link": "https://www.gog.com/en/game/brothers_a_tale_of_two_sons"
  }
]
```


### Filter Best Prices By Game Name

With the `/api/game/prices/best_prices` endpoint, you can also filter results by the name of the desired game by using the `game_name` parameter:

`GET /api/game/prices/best_prices/?to=20&game_name=witcher`

```
[
    {
        "id": 70,
        "game": {
            "id": 146,
            "name": "The Witcher 3: Wild Hunt - Hearts of Stone",
            "score": 89
        },
        "store": {
            "id": 3,
            "name": "GOG.com",
            "link": null
        },
        "price": "2.99",
        "link": "https://www.gog.com/en/game/the_witcher_3_wild_hunt_hearts_of_stone"
    },
    {
        "id": 42,
        "game": {
            "id": 69,
            "name": "The Witcher 3: Wild Hunt - Blood and Wine",
            "score": 92
        },
        "store": {
            "id": 3,
            "name": "GOG.com",
            "link": null
        },
        "price": "5.99",
        "link": "https://www.gog.com/en/game/witcher_3_wild_hunt_the_blood_and_wine_pack"
    },
    {
        "id": 20,
        "game": {
            "id": 35,
            "name": "The Witcher 3: Wild Hunt",
            "score": 93
        },
        "store": {
            "id": 3,
            "name": "GOG.com",
            "link": null
        },
        "price": "9.99",
        "link": "https://www.gog.com/en/game/the_witcher_3_wild_hunt"
    }
]
```

## Running Locally

Right now, we don't have the HerbertistAPI running online yet, but you can already run it locally!


### Requirements

To run the HerbertistAPI locally, all you really require is to have a PC with Docker up and running.


### Downloading

There are two ways you can download the HerbertistAPI source code to run locally:

- With git, all you need is to run the following command inside the folder you want to download:
```
git clone https://github.com/xlurio/hebertist-api/
```

- Without git, you'll need to download by going to the [initial page of the repository](https://github.com/xlurio/hebertist-api/), click in the `code` green button and click in `Download ZIP`. After that, all you need to do is to unzip the downloaded file inside the folder you want.


### Running

With the Docker installed, you need to run the following command inside the project folder (where is the `docker-compose.yml` file located):
```
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

Or, if you have the build-essentials or is running the project with MINGW64, you can simply run the following:
```
make run
```


### Making Requests

After that, all you need is to start making your HTTP requests in your browser, Postman or application to `http://localhost:8000/`.

P.S.: When requesting through web application, you may need to change the `CORS_ALLOWED_ORIGINS` setting on the `./api/api/settings.py` file and add the address to where your application is running from.
