# Hearmes

![the hearmes logo](https://raw.githubusercontent.com/ekavroch/hearmes/master/static/img/logo.png)

Rabbi Shaul, one of our inspiring keynote speakers during the first ever [hackathon at the Vatican](https://vhacks.org), shared the pivotal insight that what feeds the separating notion of an “Us” and a “Them” is the lack of depth, lack of a human component when we talk about unfamiliar people.

We propose a solution that humanizes migrants and refugees through a paradigm shift of how we interact with their stories, away from a context of strong negative associations. Instead, we allow their unique background to be shared with readers by injecting snippets of their writing and personality into relevant content you are already consuming, making it as easy as possible for you to make a human connection based on shared interests.

:exclamation: *This is a fork of the original repository. 
I will be trying to add extra functionality to that. I may or may not break it*

## What does Hearmes do?

Hearmes extracts the most emotionally compelling phrase in a given text and converts it to an embeddable bite-sized HTML snippet. That snippet
can then be placed into related content throughout the web (either manually or through using ad spaces)

## How does Hearmes work?

1) Submitting a story is as easy as handwriting it and scanning to upload, where a computer vision API converts the image to text format.
2) Using natural language processing, our system extracts keywords relevant to the story and also determines, through a proprietary method,
the most compelling phrase in the story that can be placed into related content throughout the web.
3) Supporting websites can search through our code for keywords relevant to their content and obtain an HTML snippet
that is easily embedable. Here is an example - as a jazz enthusiast, I’m reading a recent review in a prominent newspaper,
when I stumble upon this attention-grabbing quote. I’m driven to click to read more, 
and just like that I’ve had a moment of connection with a migrant in my area!

If you need something more comprehensive, [there's a detailed video demo]() 

## How did you build this?

You can find more information on that [on the Devpost project page](https://raw.githubusercontent.com/ekavroch/hearmes/master/static/img/logo.png)

## What's next for Hearmes? 

1) Hopefully adding support for other alphabets for now

## That's quite useful! Is it okay to use this?

Absolutely! Feel free to remix and adapt as you like 


## License

This project is licensed under the MIT license. A copy of the license is included in `LICENSE.md`. If you have any questions regarding this license or any other Open Source licenses, you can reference [this handy website](https://itsfoss.com/open-source-licenses-explained/) that goes into great detail regarding everything license-wise!

## Other Credits

[The untweaked form design](https://colorlib.com/wp/template/contact-form-v2/) is available for free under the `CC BY 3.0` [license](https://creativecommons.org/licenses/by/3.0/).
Most of this README can also be found on our [Devpost Project Page](devpost.com/software/hearmes)