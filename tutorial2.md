#### Patterns in Extepmore
Today you'll be making music with a code structure in Extempore called patterns. We'll break down a pattern into its components and outline a few ways you can use it. This way, you can get stuck into making some sweet music, which is really why you're here. :)

Below is an example of a pattern. Copy this code into your canvas.xtm file. You can evaluate this line by placing your cursor within its scope and hitting `ctr`+`Enter`. It should be playing some music, yes? Great! Now, you can try changing some of the numeric values in the pattern. Evaluate the pattern between changes to see how they affect what you're hearing. I should point out that the value following the *'@1'*, currently set to '80', controls the volume. Operate with care.

``` Scheme
(:> A 4 0 (play syn1 @1 80 dur) '(60 63 67 72))
```

After some playing around, you may have gained an intuition to how the different parts of this code structure affect the sounds you're hearing. So here are the different components. 
- `'(60 63 67 72)`: The latter part of the pattern is a list of midi pitches. Incrementing a midi pitch by 1 raises its pitch by a semitone. Based on the other arguments passed to the pattern, Extempore will loop through this list and play the pitches within the list.
This list can be replaced with any function which returns a list. For example, we can reverse this list `(reverse '(60 63 67 72))` or rotate the elements to the right by two elements 
`(rotate '(60 63 67 72) 2)`.
- `:>` this symbol tells Extempore to start playing the pattern. You can stop playing a pattern by replacing it with `:|`
- `A`: This is just a name to give the pattern.
- Then you have two values following the pattern name. The first number determines how many beats it takes to move through the entire list. So if this value is 4 and there are 4 pitches in your list, each pitch will be played on a beat. The second value marks the offset from the beginning of the list. At the beginning of each loop, Extempore will start playing the pitch at this offset.
- `play function`: specifies some information required to play a single pitch. 
    - syn1: the type of instrument. Here we have a synthesizer. You can replace this with any predefined instrument in Extempore. 
            The instruments we have today are *syn1*, *samp1* (a piano) and *kit* (a drum kit). The pitches in the drum kit will refer to parts of the drum kit (hi-hat, kick etc.) 
    - @1: an index into which list to start playing from. You can infact have multiple lists at the end of your pattern and index into them using this parameter. The indices start from 1.
    - volume: The volume
    - dur: the duration each pitch is played for. You can extract fractions of this duration with prefix notation. For example, replacing this with `(* 0.5 dur)` will play the note for half the duration.

##Rhythm and Harmony
Here is a list of a few other things patterns are capable of. You can just have a read through this list and come back to it at the end, when you start making your music. 

##### Add rests
Wherever the `_` symbol appear within the list, Extempore will treat this as a rest.
``` Scheme
(:> A 4 0 (play syn1 @1 80 dur) '(60 63 _ 67 72))
```

##### Randomness
If you want to add some stochasticity, you can use the random function. The random function in Extempore is overloaded and can be invoked in the following ways.

No arguments: This will generate a floating point number between 0 and 1. 
``` Scheme
(random)
```

With a list: This will select a random element from the list.
``` Scheme
(random '(30 40 35))
```

With two integers: This will select a number in the range of these two arguments. 
``` Scheme
(random 60 90)
```


##### Add nested lists
Allows you to control when each pitch is played. Since the list below is played over 4 beats, pitch 67 and 72 will be played on the second and fourth beat respectively and the inner lists (60 63) and (75 75) will be played on beat 1 and 3. So each pitch within the inner lists will be played for half beats and will be played one after the other.
``` Scheme
(:> A 4 0 (play syn1 @1 80 dur) `((60 63) 67 (75 75) 72))
```

##### Add harmony
You can sound two pitches at the same time with the `#` symbol. 
``` Scheme
(:> A 4 0 (play syn1 @1 80 dur) `(#(60 63) 67 #(75 75) 72))
```

##### Instrument examples

Drums:
```Scheme
(:> C 4 0 (play kit @1 80 dur) `(12 #(12 24) 12 #(12 24)))
```

Piano:
```Scheme
(:> A 4 0 (play syn1 @1 80 dur) `((c4 d4) eb4 (g4 (a4 bb4)) c5))
```

## Let's Make Some Tunes
Okay, this should be enough to let you loose and have you start making some music. Feel free to copy and paste any examples in this document to your canvas.xtm file to get you started. You can keep making music for upto 30 mins. You don't have to use the full 30 mins, but try to see if you can go for at least 10 mins. If you've had your fun before the time is up,
let me know. Also, I hope you don't mind if I listen in on what you're creating. I'm not assesing how 'good' the music you're making is. I'm just curious to see (and hear) what you create :)



Here is a link to a [midi-pitch chart](https://newt.phys.unsw.edu.au/jw/notes.html) mapping midi pitches to piano keys which might come in handy.

Have fun :)