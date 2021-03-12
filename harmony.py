################
# Core Classes #
################

class Scale:
    """
    A scale contains the name of the scale and intervals between notes.
    Intervals are measured with respect to the convention that a value of one
    corresponds to one semitone in Western tonal music. Assumes intervals
    repeat. Assumes the scale is strictly ascending.

    ...

    Attributes
    ----------
    name : str
        the name of the scale
    intervals : tuple
        the tuple of intervals in one cycle of the scale
    chords : dictionary
        a dictionary where the key is a chord and value is a set of indices in
        the scale corresponding to the start of the chord

    Methods
    -------
    num_notes()
        Returns the number of notes in the scale.
    has_chord(chord)
        Returns whether a given type of chord exists in the scale.
    add_chord(chord)
        Adds a given type of chord to the scale to all possible base notes if it
        can be validly added.

    interval_between(i,j)
    """

    def __init__(self, name, intervals):
        """
        Constructs all the necessary attributes for a scale object.

        Parameters
        ----------
            name : str
                the name of the scale
            intervals : tuple
                tuple of intervals in one cycle of the scale
        """

        self.name = name
        self.intervals = intervals
        self.chords = {}

    def num_notes(self):
        """Returns the length of a cycle of notes in the scale."""
        return len(self.intervals)

    def has_chord(self, chord):
        """
        Checks if a given CHORD exists in CHORDS and memoizes it if it exists.
        Returns whether or not the chord exists

        Parameters
        ----------
            chord : Chord
                the chord we are checking.

        Returns
        -------
        bool
        """
        if chord.name in self.chords and len(self.chords[chord.name]) > 0:
            return True
        elif chord.name in self.chords and len(self.chords[chord.name]) == 0:
            return False
        else:
            return self.add_chord(chord)

    def add_chord(self, chord):
        """
        Adds a given CHORD to CHORDS if it exists in the scale. Returns a
        boolean indicating whether it found the chord in the scale.

        Parameters
        ----------
            chord : Chord
                the chord type we are adding.

        Returns
        -------
        bool
        """

        self.chords[chord.name] = set()

        chord_added = False

        for base_note in range(0, self.num_notes()):
            # For each base note, check to see if chord fits in at that
            # position.

            illegal_chord = False
            i = base_note

            for current_interval in chord.intervals:
                # Run through intervals starting from the base note to see if it
                # matches up. Keep track of a running sum from "checkpoints" in
                # our traversal of the scale to see if the next interval fits.

                accumulated_interval = 0

                while True:
                    accumulated_interval += self.intervals[i]
                    i += 1
                    i %= self.num_notes()

                    if accumulated_interval == current_interval:
                        break
                    elif accumulated_interval > current_interval:
                        illegal_chord = True
                        break

            if not illegal_chord:
                self.chords[chord.name].add(base_note)
                chord_added = True

        return chord_added

    def interval_between(self, i, j):
        """
        Returns the size of the interval between notes at indices i and j. We do
        not expect i and j to be expressed modulo the number of notes --
        anything greater than or equal to the number of notes is treated as if
        we repeated the scale using the same intervals.

        Parameters
        ----------
            i : int
                the index of the one note.
            j : int
                the index of the other note.

        Returns
        -------
        int
        """

        if (i > j):
            i, j = j, i

        accumulated_interval = 0

        for k in range(0, j - i):
            accumulated_interval += self.intervals[(i + k) % self.num_notes()]

        return accumulated_interval


class Chord:
    """
    A chord contains the name of the chord (or chordioid) and intervals between
    notes.

    ...

    Attributes
    ----------
    name : str
        the name of the chord
    intervals : tuple
        list of intervals in the chord
    """

    def __init__(self, name, intervals):
        """
        Constructs all the necessary attributes for a scale object.

        Parameters
        ----------
            name : str
                the name of the scale
            intervals : tuple
                the tuple of intervals in one cycle of the scale
        """

        self.name = name
        self.intervals = intervals

major_scale = Scale("Major", [2,2,1,2,2,2,1])
minor_scale = Scale("Minor", [2,1,2,2,1,2,2])
melodic_minor = Scale("Melodic Minor", [2,1,2,2,1,3,1])
harmonic_minor = Scale("Harmonic Minor", [2,1,2,2,2,2,1])

major_chord = Chord("Major", [4,3])
minor_chord = Chord("Minor", [3,4])
dim_chord = Chord("Diminished", [3,3])
aug_chord = Chord("Augmented", [4,4])
sus2_chord = Chord("Sus2", [2,5])
sus4_chord = Chord("Sus4", [5,2])

scales = [major_scale, minor_scale, melodic_minor, harmonic_minor]
chords = [major_chord, minor_chord, dim_chord, aug_chord, sus2_chord, sus4_chord]

for scale in scales:
    for chord in chords:
        scale.add_chord(chord)

    print(scale.name + "::\n" + str(scale.chords) + "\n")

def chordal_relationships(scale_1, scale_2, chord):
    fifths_relations = set()
    if scale_1.has_chord(chord) and scale_2.has_chord(chord):
        for root_1 in scale_1.chords[chord.name]:
            for root_2 in scale_2.chords[chord.name]:
                dist_1 = scale_1.interval_between(0,root_1)
                dist_2 = scale_1.interval_between(0,root_2)
                key_distance = dist_2 - dist_1
                print("Distance between {0} to {1} (via {2} chord at {3} for the first scale to {4} of the second scale) (Looking where Scale 2 is relative to Scale 1) is {5} fifths right, or {6} fourths left or, or semitones right.\n".format(
                    scale_1.name,
                    scale_2.name,
                    chord.name,
                    root_1 + 1,
                    root_2 + 1,
                    (key_distance * 7) % 12,
                    (12 - ((key_distance * 7) % 12)) % 12,
                    key_distance % 12
                ))
                fifths_relations.add((key_distance * 7) % 12)

    print("Using the {0} chord, we can reach {1}\n".format(chord.name, str(fifths_relations)))

def all_chordal_relationships(scale_1, scale_2):
    for chord in chords:
        chordal_relationships(scale_1, scale_2, chord)