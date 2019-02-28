from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.layout import Layout, Fieldset

from core.forms import horizontal_form_helper
from programme.forms import AlternativeProgrammeFormMixin
from programme.models import Programme

from .models import SignupExtra


FIELD_TEXTS = dict(
    title=(_('Game title'), None),
    rpg_system=(_('RPG system'), _('Which RPG system does the game use?')),
    approximate_length=(_('Game length (minutes)'), None),
    min_players=(_('Minimum number of players'), _('Pelaajien vähimmäismäärä')),
    max_players=(_('Maximum number of players'), None),
    is_in_english=(_('In English'), _('Please tick this box if the game is played in English.')),
    is_age_restricted=(_('Ages 18+ only'), _('Please tick this box if your game contains themes which require it to be restricted to players who are 18+ years old. Please give more details in the game description.')),
    is_children_friendly=(_('Suitable for children'), _('Please tick this box if your game is also suitable for children. If necessary, you can give more details in the game description.')),
    is_family_program=(_('Family program'), _('Please tick this box if your game has been designed also for the youngest players, and the players’ guardians may help the players or participate in the game with them. If necessary, you can give more details in the game description.')),
    is_intended_for_experienced_participants=(_('For experienced players'), _('Check this if the game requires knowledge of the world or the rules of the game.')),
    description=(_('Description'), _('Advertise your game to potential players. Be extra sure to inform about potentially shocking or disturbing themes. Recommended length is 300–500 characters. We reserve the right to edit the text as necessary.<br><br>Please write the description at least in the language the game will be run in (English or Finnish). You may include the description in both languages, if you wish.')),
    three_word_description=(_('Short blurb'), _('Summarize your game in one sentence which helps potential players get the gist of your game. For example, “Traditional D&D dungeon adventure” or “Lovecraftian horror in Equestria”. We reserve the right to edit the text.')),
    notes_from_host=(_('Other information for the RPG coordinator'), _('If there is anything else you wish to say to the RPG coordinator that is not covered by the above questions, please enter it here.')),
)


class SignupExtraForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'shift_type',

            Fieldset('Työtodistus',
                'want_certificate',
                'certificate_delivery_address',
            ),
            Fieldset('Lisätiedot',
                'special_diet',
                'special_diet_other',
                'prior_experience',
                'shift_wishes',
                'free_text',
            )
        )

    class Meta:
        model = SignupExtra
        fields = (
            'shift_type',
            'want_certificate',
            'certificate_delivery_address',
            'special_diet',
            'special_diet_other',
            'prior_experience',
            'shift_wishes',
            'free_text',
        )

        widgets = dict(
            special_diet=forms.CheckboxSelectMultiple,
        )

    def clean_certificate_delivery_address(self):
        want_certificate = self.cleaned_data['want_certificate']
        certificate_delivery_address = self.cleaned_data['certificate_delivery_address']

        if want_certificate and not certificate_delivery_address:
            raise forms.ValidationError('Koska olet valinnut haluavasi työtodistuksen, on '
                'työtodistuksen toimitusosoite täytettävä.')

        return certificate_delivery_address


class ProgrammeSignupExtraForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = horizontal_form_helper()
        self.helper.form_tag = False

    class Meta:
        model = SignupExtra
        fields = (
            'special_diet',
            'special_diet_other',
        )

        widgets = dict(
            special_diet=forms.CheckboxSelectMultiple,
        )


class RpgForm(AlternativeProgrammeFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event')
        admin = kwargs.pop('admin') if 'admin' in kwargs else False

        super().__init__(*args, **kwargs)

        self.helper = horizontal_form_helper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'title',
            'rpg_system',
            'approximate_length',
            'min_players',
            'max_players',
            'is_revolving_door',
            Fieldset(_('Who is the game meant for?'),
                'is_in_english',
                'is_age_restricted',
                'is_children_friendly',
                'is_family_program',
                'is_beginner_friendly',
                'is_intended_for_experienced_participants',
            ),
            Fieldset(_('Game genre (Choose all which apply)'),
                'ropecon2018_genre_fantasy',
                'ropecon2018_genre_scifi',
                'ropecon2018_genre_historical',
                'ropecon2018_genre_modern',
                'ropecon2018_genre_war',
                'ropecon2018_genre_horror',
                'ropecon2019_genre_adventure',
                'ropecon2018_genre_mystery',
                'ropecon2018_genre_drama',
                'ropecon2018_genre_humor',
            ),
            Fieldset(_('Game style (Choose any which apply)'),
                'ropecon2018_style_serious',
                'ropecon2018_style_light',
                'ropecon2018_style_rules_heavy',
                'ropecon2018_style_rules_light',
                'ropecon2018_style_story_driven',
                'ropecon2018_style_character_driven',
                'ropecon2018_style_combat_driven',
                'description',
                'three_word_description',
                'ropecon2019_blocked_time_slots',
                'notes_from_host',
            )
        )

        for field_name, (label, help_text) in FIELD_TEXTS.items():
            self.fields[field_name].label = label
            self.fields[field_name].help_text = help_text

    class Meta:
        model = Programme
        fields = [
            'title',
            'rpg_system',
            'approximate_length',
            'min_players',
            'max_players',
            'is_revolving_door',

            # Who is the game meant for?
            'is_in_english',
            'is_age_restricted',
            'is_children_friendly',
            'is_family_program',
            'is_beginner_friendly',
            'is_intended_for_experienced_participants',

            # Genre
            'ropecon2018_genre_fantasy',
            'ropecon2018_genre_scifi',
            'ropecon2018_genre_historical',
            'ropecon2018_genre_modern',
            'ropecon2018_genre_war',
            'ropecon2018_genre_horror',
            'ropecon2019_genre_adventure',
            'ropecon2018_genre_mystery',
            'ropecon2018_genre_drama',
            'ropecon2018_genre_humor',

            # Style
            'ropecon2018_style_serious',
            'ropecon2018_style_light',
            'ropecon2018_style_rules_heavy',
            'ropecon2018_style_rules_light',
            'ropecon2018_style_story_driven',
            'ropecon2018_style_character_driven',
            'ropecon2018_style_combat_driven',

            'description',
            'three_word_description',
            'ropecon2019_blocked_time_slots',
            'notes_from_host',
        ]

        widgets = dict(
            ropecon2019_blocked_time_slots=forms.CheckboxSelectMultiple,
        )

    def get_excluded_field_defaults(self):
        return dict(
            category=Category.objects.get(event__slug='ropecon2019', slug='roolipeli'),
        )
