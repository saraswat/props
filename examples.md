# Generating logical form from sentences, using propS

I have implemented a nested logical form generator, built around the core relations in propS. It leverages propS's core
ability to identify (possibly multiple) propositions in a sentence, while removing much of the syntactical clutter that
plagues other approaches. 

(My work was fairly straightforward -- simply about generating a nested json (unordered) structure, with
explicit cross-references in cases where the same node is targeted by multiple parents.)

## Examples
```
{'lf': {'comp': {'dobj': 'issue', 'pred': 'combat', 'subj': {'xref': '21'}},
        'iobj': {'dep': {'conj_and': ['staffing',
                                      {'mod': ['national', 'specific'],
                                       'word': ['anti-drugs', 'agency']}],
                         'pred': 'and'},
                 'prep_in': ['security', 'force'],
                 'word': 'increase'},
        'pred': 'proposed',
        'subj': {'word': ['Mr', 'Macri'], 'xtarget': '21'}},
 'sentence': 'Mr Macri has proposed an increase in security force staffing , and a specific national anti-drugs agency to combat the issue .'}

```

```
{'lf': {'comp': [{'comp': {'pred': 'rule', 'prep_by': 'decree'},
                  'dobj': {'mod': 'presidential', 'word': 'power'},
                  'pred': 'limit',
                  'subj': {'xref': '25'}},
                 {'dobj': {'prep_of': {'conj_and': [{'mod': {'pred': 'stalled'},
                                                     'word': ['reform',
                                                              'agenda']},
                                                    {'mod': 'legislative',
                                                     'word': 'gridlock'}],
                                       'pred': 'and'},
                           'word': 'possibility'},
                  'pred': 'creating'}],
        'pred': 'seeks',
        'subj': {'word': 'legislature', 'xtarget': '25'}},
 'sentence': 'The legislature seeks to limit presidential power to rule by decree , creating the possibility of legislative gridlock and a stalled reform agenda .'}
```

```
{'lf': [{'mod': 'also',
         'pred': 'modified',
         'prepc_by': {'dobj': [{'word': ['Media', 'Law'], 'xtarget': '71'},
                               {'prep_of': {'mod': [{'mod': 'more',
                                                     'word': 'controversial'},
                                                    {'pred': 'passed',
                                                     'prep_by': ['Fernandez',
                                                                 'administration']}],
                                            'word': 'reforms'},
                                'word': 'one',
                                'xtarget': '59'}],
                      'word': 'decree'},
         'subj': ['Mr', 'Macri']},
        {'pred': 'SameAs', 'sameAs_arg': [{'xref': '71'}, {'xref': '59'}]}],
 'sentence': 'Mr Macri also modified by decree the Media Law , one of the more controversial reforms passed by the Fernandez administration .'}
```

```
{'lf': {'dobj': {'comp': {'obj': ['decree', 'powers'],
                          'pred': 'eliminated',
                          'prep_at': 'point',
                          'prep_during': ['President',
                                          'Mauricio',
                                          'Macris',
                                          'administration']},
                 'word': 'risk'},
        'pred': 'raises',
        'subj': {'prep_of': {'prep': {'pcomp': {'pobj': {'mod': 'dominant',
                                                         'word': ['Peronist',
                                                                  'party']},
                                                'word': 'outside'},
                                      'word': 'from'},
                             'word': 'president'},
                 'word': 'election'}},
 'sentence': 'The election of a president from outside the dominant Peronist party raises the risk that decree powers will be eliminated at some point during President Mauricio Macris administration .'}
```

Note — this one is quite complicated! The graph has a cycle in it.

```
{'lf': [{'prep_of': {'xref': '112'},
         'top': 0,
         'word': 'number',
         'xtarget': '110'},
        {'dobj': {'xref': '112'},
         'pred': 'overturned',
         'subj': ['Mr', 'Macri'],
         'xtarget': '113'},
        {'mod': {'xref': '113'},
         'prep_on': ['media', 'holdings'],
         'top': 0,
         'word': 'restrictions',
         'xtarget': '112'},
        {'dobj': {'xref': '110'}, 'pred': 'placed', 'subj': 'law'}],
 'sentence': 'The law had placed a number of restrictions on media holdings , which Mr Macri has overturned .'}
```
