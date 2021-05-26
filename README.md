# fillmask
Returns tokens for the masks in the given text.

This is intended to be deployed as a web service.  
Try it out here:  
    - GET https://ajh-fillmask.herokuapp.com/fillmask?text=A%20%5BMASK%5D%20is%20found%20to%20be%20convenient%20by%20many%20owners%20of%20companion%20animals%2C%20especially%20dogs%20and%20cats%2C%20because%20it%20lets%20the%20pets%20come%20and%20go%20as%20they%20please%2C%20reducing%20the%20need%20for%20pet-owners%20to%20let%20or%20take%20the%20pet%20outside%20manually%2C%20and%20curtailing%20unwanted%20behaviour%20such%20as%20loud%20vocalisation%20to%20be%20let%20outside%2C%20scratching%20on%20doors%20or%20walls%2C%20and%20%28especially%20in%20the%20case%20of%20dogs%29%20excreting%20in%20the%20house.  
    - GET https://ajh-fillmask.herokuapp.com/fillmask/A%20%5BMASK%5D%20is%20found%20to%20be%20convenient%20by%20many%20owners%20of%20companion%20animals%2C%20especially%20dogs%20and%20cats%2C%20because%20it%20lets%20the%20pets%20come%20and%20go%20as%20they%20please%2C%20reducing%20the%20need%20for%20pet-owners%20to%20let%20or%20take%20the%20pet%20outside%20manually%2C%20and%20curtailing%20unwanted%20behaviour%20such%20as%20loud%20vocalisation%20to%20be%20let%20outside%2C%20scratching%20on%20doors%20or%20walls%2C%20and%20%28especially%20in%20the%20case%20of%20dogs%29%20excreting%20in%20the%20house.  
    - https://ajh-fillmask.herokuapp.com/graphql  


### Example input
```
A [MASK] is found to be convenient by many owners of companion animals, especially dogs and cats, because it lets the pets come and go as they please, reducing the need for pet-owners to let or take the pet outside manually, and curtailing unwanted behaviour such as loud vocalisation to be let outside, scratching on doors or walls, and (especially in the case of dogs) excreting in the house.
```


### Example output
```json
{
    "data": {
        "suggestions": [
            [
                {"text":"house", "score":0.1014120951294899}
            ],
            [
                {"text":"cat", "score":0.03469451144337654}
            ],
            ...
        ]
    }
}
```
