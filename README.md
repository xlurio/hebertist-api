# HebertistAPI

Welcome to the Hebertist REST API! This API was made with the propose of making easier to us, mere peasants, to buy games with lower prices by comparing the price of a variety of games in multiple stores. Here are some of the features already running:

- Retrieve the rank of lowest prices from the `N`th to the `K`th to the element in the database;
- Filter best prices by the name of the game;
- See the price historic of a game;
- Update game prices every three days;
- Update list of games every month;

## Summary

- [Retrieve Prices](#retrieve-prices)

  - [Filter Prices By Game ID](#filter-prices-by-game-id)
  - [Filter Prices By Price Upper Bound](#filter-prices-by-price-upper-bound)

- [Retrieve The Best Prices Only](#retrieve-the-best-prices-only)

  - [Retrieve Best Price](#retrieve-best-price)
  - [Get Best Price By Game ID](#get-best-price-by-game-id)
  - [Filter Best Prices By Game Name](#filter-best-prices-by-game-name)

- [Retrieve Price Historic](#retrieve-price-historic)

  - [Retrieve All Price Historic](#retrieve-all-price-historic)
  - [Filter Price Historic By Game ID](#filter-price-historic-by-game-id)
  - [Get Lowest Price In History](#get-lowest-price-in-history)

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
```

For performance purposes, this endpoint is paged. To navigate between pages, you can use the parameter `page` like this: `/api/game/prices/?page=[n]`, where `[n]` is the page number you desire.

### Filter Prices By Game ID

### Filter Prices By Price Upper Bound

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

### Get Best Price By Game ID

### Filter Best Prices By Game Name

### Filter Prices By Price Upper Bound

## Retrieve Price Historic

If want to know if you are taking the best offer, you can check on the historic of prices on the `api/historic/prices`, where

### Retrieve All Price Historic

### Filter Price Historic By Game ID

### Get Lowest Price In History

## Running Locally

### Requirements

### Downloading

### Running

### Making Requests
