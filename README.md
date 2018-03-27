# YAML trainer for [Wit.ai](https://wit.ai)

Auto Train your wit.ai bot using YAML format dataset. The purposes of making this program are:
- Avoiding submitting one-by-one your data through the Web GUI
- Minimize the use of code when training your bot
- Make it easier to train using entities tagged data

## Prerequisites

This program runs on Python 2 or Python 3 and needs some requirements written in requirements.txt. Install it using the command below (after you install pip on your system):

```
pip install -r requirements.txt
```

## Bot Preparation

0. Create your bot first through the web wit ai, then get the BEARER code in the setting menu.

1. Open config.yaml, write your BEARER code and version (the latest date) here

      Example:

    ```
    config:
      bearer: NKPU6CR7SCIHUZ5NR4762E2WXLQ6V3IP
      version: 15/01/2018
    ```

2. Create a Yaml dataset file (for example see dataset.yaml) which contains:
    - `definition`
    - `data`
    -  `start` (optional)
    -  `end` (optional)

    see description below for details of each key
    

    ### `definition`

    Define abbreviations of your intents and entities name in this section. This abbreviation will make it easier for you when labeling the entities of your  data later. 

    ---
    **WARNING**

    You can use any letter to make abbreviation. But to distinguish between intents and entities is **required** to start the abbreviation for the intents with the letter 'i'. So, the first letter of an abbreviation is 'i' if and only if it represents an intent.

    ---

    Example:

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

    #### Usage

    To use those abbreviations in your dataset, use backslash '\\' before the part of the sentence you want to tag (LaTeX style). Use format `\abbrevations{tagged_text}`.
    
    For example, if you have a sentence below and a list of abbreviations above. 

    ```
    Set the date to 5 Feb, please
    ```

    to define the intent to "set", tag the whole sentence with set intent (`is`) abbreviation with formats like the example below:

    ```
    \is{Set the date to 5 Feb, please}
    ```

    Then, to define the date entities, tag the date part of the sentence with `d`:

    ```
    \is{Set the date to \d{5} Feb, please}
    ```

    If you are using [keyword entities](https://wit.ai/docs/recipes#extract-a-keyword-entity) in wit.ai you can assign a different value to an entity (which allows you to create synonims of keyword). To do that, add additional brackets right after tagged part of the sentence. Use format `\abbrevations{tagged_text}{assigned_value}`.
    
    In the example below we will tag "Feb" as month entities, but we assign it with value "february":

    ```
    \is{Set the date to \d{5} \m{Feb}{february}, please}
    ```

    After you run it, the example above will train your bot with a data below:

    ```
    text : Set the date to 5 Feb, please
    intent : set
    date : 5
    month : february
    ```


    ### `data`

    Write your dataset in this section. There are two styles to write your dataset, numbered dataset or not numbered dataset. And each train, you should only use one style.

    ---
    **WARNING**

    In each training you are only allowed to use one style of dataset

    ---

    #### Numbered dataset
    Numbered dataset needs another two keys: `start` and `end`, to define the start and the end of the part of data to be trained. It will be useful to avoid accidental redundancy of data train when training your bot. If you define the value of `end` with -1 then the data to be trained starts from the numbered data defined in `start` to the last. `start` and `end` are inclusive.

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

    #### Unnumbered dataset
    The second type will always train the bot with all of your data (be careful with redundancy if you train your bot multiple times).

    ```
    data:
      - \ig{Good afternoon guys!}
      - \ia{Who are you again?}
      - \is{Give me any information about \n{Gil}{Gilfoyle}}
      - \is{where is I can find King \n{Dinesh}}?
    ```

## Bot Training

After define everything in config.yaml, simply train your bot by running the following command in the same directory with app.py and config.yaml:

```
python app.py dataset_name
```
replace `dataset_name` with your dataset file name (with or without *.yaml)

## Example

You can see the example in config.yaml and dataset.yaml. Or run this repo using command:
```
python app.py dataset
```