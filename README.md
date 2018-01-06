# YAML trainer for [Wit.ai](https://wit.ai)

Auto Train your wit.ai bot using YAML format dataset. This program is created to aims:
- Avoiding one-by-one put your sentence into Web GUI
- Minimizing "code-interaction" and "code-formatting" when training your bot
- Easily to train with entities tagged data

## Prerequisites

This program run on Python 3 and need some requirements written in requirements.txt. Install it using the command below (after you install pip on your system):

```
pip install -r requirements.txt
```

## Setting

Before you start to train your bot, first you need to create your bot using Web GUI of wit.ai, then get the BEARER code in settings menu.

Then, Open config.yaml which contains 3 following keys

   - `config`
   - `definition`
   - `data`

### `config`

Write your BEARER code and version (latest date you train your bot) here

```
config:
  bearer: 6RELTMESF23TMQCWJQVXQZGLPHHDX7ZJ
  version: 05/01/2018
```

### `definition`

Define abbreviation (codename) of your intents and entities name. The definition will make it easier to write entities in the dataset. You can use any letter or number to define a codename. But, to differentiate the intent and the entities, it is **mandatory** to write intent codename with a lowercase 'i' for the first character.

```
definition:
  # INTENTS
  is: set
  iu: update
  ih: show
  # ENTITIES
  d: date
  m: month
  t1: hours
  t2: minutes
```
To use those definitions in your dataset use backslash '\\' before the tagged part of a sentence (LaTeX style). For example, if you have a sentence below and a definition above. 

```
Set the date to 5 Feb, please
```

to define the intention to set a date, tag the sentence with set intent (`is`) codename. Close it with curly bracket, and put codename before it:

```
\is{Set the date to 5 Feb, please}
```

then define the date entities, with the same rules:

```
\is{Set the date to \d{5} Feb, please}
```
If you are using keyword entities in wit.ai you can give specific value to an entities. To do that, create additional bracket just after tagged part of a sentence, then define the returned value. In the example below we tag "Feb" as month entities, with  keyword value "february":

```
\is{Set the date to \d{5} \m{Feb}{february}, please}
```

### `data`

Write your dataset here. There are two styles to write your dataset, numbered dataset or not numbered dataset. And each train, you should only use one style.

Numbered dataset need another two keys `start` and `end` to define which data will be trained. It intended to prevent unintentionally redundancy when training your bot. If you define `end` with -1 it will train your data from number defined in `start` until the last data. `start` and `end` are inclusive.

```
start: 1
end: -1
data:
  1: \ig{Good morning guys!}
  2: \ia{Who are you?!!}
  3: \is{Give me information about \n{Gilfoyle}}
  4: who is \n{Dinesh}?
  5: who are you \n{dinesh}{Dinesh}?
```

The second type will always train all of your data (becareful with redundancy if you train multiple times).

```
data:
  - \ig{Good afternoon guys!}
  - \ia{Who are you again?}
  - \is{Give me any information about \n{Gil}{Gilfoyle}}
  - \is{where is I can find King \n{Dinesh}}?
```

## Usage

After defining everything in config.yaml, simply train your bot by running the following command in the same directory with app.py and config.yaml:

```
python3 app.py
```

## Example

You can see the example in config.yaml
