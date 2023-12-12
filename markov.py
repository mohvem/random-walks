# This file defines a Markov object that we can use to identify who said a particular speech.

# Name: Mohini
from math import log
import pathlib
HASH_CELLS = 57
TOO_FULL = 0.5
GROWTH_RATIO = 2


def calc_substr(text, lookfwd_num):
    ''' 
    This function takes a given string and outputs all the substrings
    according to Markov logic in a list

    Input: Text and number to create k-length substrings of.

    Output: List of substrings of length lookfwd_num
    '''
    all_strings = []
    for index, substr in enumerate(text):
        out_str = ''
        # Case 1: Will reach end of text and need to loop around to front
        if index + lookfwd_num - 1 > len(text) - 1:
            # Add what is left of string
            out_str += text[index:]
            # Loop back around for rest
            out_str += text[:(lookfwd_num - len(text[index:]))]
        # Case 2: Have enough string, just go lookfwd_num forward from current
        else:
            out_str += text[index:(index+lookfwd_num)]
        all_strings.append(out_str)
    return all_strings

class Markov:
    def __init__(self, k, text):
        """
        Construct a new k-order markov model using the text 'text'.
        """
        self.k = k
        self.text = text
        self.s = len(set(self.text))


    def build_hashtable(self, lookforward_num):
        '''
        This function takes a text and an input
        and calculates the hashtable of the key-value pairs of the k + k-1 strings
        and how often they show up

        Inputs:
        Markov object and how many forward to look in the string

        Output:
        Hashtable of the key-value pair of string and how often
        '''
        # Calculate the string subsets
        substrings = calc_substr(self.text, lookfwd_num=lookforward_num)

        # Instantiate the hashtable and update with values if strings match
        outhashtable = {substr:0 for substr in substrings}
        for substr in substrings:
            outhashtable[substr] += 1
        return outhashtable

    def log_probability(self, s):
        """
        Get the log probability of string "s", given the statistics of
        character sequences modeled by this particular Markov model
        This probability is *not* normalized by the length of the string.

        Input: Markov object and speech to calculate probabilities
        """
        # Initialize the hashtables and identify substrings for the unknown case
        known_hash_k = self.build_hashtable(lookforward_num= self.k)
        known_hash_k_1 = self.build_hashtable(lookforward_num= self.k + 1)
        s_strings_k = calc_substr(s, lookfwd_num= self.k)
        s_strings_k_1 = calc_substr(s, lookfwd_num= self.k + 1)

        # Calculate the probability the unknown is from that speech
        n_values = [known_hash_k.get(s_k) or 0 for s_k in s_strings_k]
        m_values = [known_hash_k_1.get(s_k_1) or 0 for s_k_1 in s_strings_k_1 ]
        probs = [log( (m_values[i] + 1) / (n_values[i] + self.s)) for i in range(len(n_values))]
        return sum(probs)

def identify_speaker(speech1, speech2, speech3, k):
    """
    Given sample text from two speakers (1 and 2), and text from an
    unidentified speaker (3), return a tuple with the *normalized* log probabilities
    of each of the speakers uttering that text under a "order" order
    character-based Markov model, and a conclusion of which speaker
    uttered the unidentified text based on the two probabilities.

    Input: known speech1, known speech2, unknown speech3, look forward number
    and whether to use hashtable or dictionary

    Output: Tuple with probability speech3 is from speech1, probability speech3
    is from speech2, and which speaker it is
    """
    ### Learn Markov models for the known speeches
    speech1_model = Markov(k=k, text= speech1)
    speech2_model = Markov(k=k, text= speech2)

    ### Calculate probability of speech 3 from each
    speech1_prob = speech1_model.log_probability(s=speech3) / len(speech3)
    speech2_prob = speech2_model.log_probability(s=speech3) / len(speech3)

    ### Determine which probability is higher
    if speech1_prob > speech2_prob:
        speaker_name = 'A'
    else:
        speaker_name = 'B'
    return (speech1_prob, speech2_prob, speaker_name)