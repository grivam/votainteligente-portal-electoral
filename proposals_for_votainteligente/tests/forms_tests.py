# coding=utf-8
from popular_proposal.tests import ProposingCycleTestCaseBase
from popular_proposal.forms import (CommentsForm,
                                    RejectionForm,
                                    ProposalTemporaryDataUpdateForm,
                                    ProposalTemporaryDataModelForm,
                                    FIELDS_TO_BE_AVOIDED,
                                    AuthorityNotCommitingForm)
from popular_proposal.forms.form_texts import TOPIC_CHOICES_DICT
from django.contrib.auth.models import User
from django.forms import CharField
from popular_proposal.models import (ProposalTemporaryData,
                                     PopularProposal)
from django.core import mail
from django.template.loader import get_template
from django.template import Context, Template
from popular_proposal.forms import (WHEN_CHOICES,
                                    AuthorityCommitmentForm)
from popular_proposal.forms.form_texts import TEXTS
from django.core.urlresolvers import reverse
from elections.models import Area, Election
from django.test import override_settings
from constance.test import override_config
from proposals_for_votainteligente.forms import (ProposalWithAreaForm,
                                                 UpdateProposalForm,
                                                 AreaForm)



class FormsWithAreaTestCase(ProposingCycleTestCaseBase):
    def setUp(self):
        super(FormsWithAreaTestCase, self).setUp()

    def test_instanciate_form(self):
        original_amount = len(mail.outbox)
        form = ProposalWithAreaForm(data=self.data,
                                    proposer=self.fiera,
                                    area=self.arica)
        self.assertTrue(form.is_valid(), form.errors)
        cleaned_data = form.cleaned_data
        temporary_data = form.save()
        self.assertEquals(len(mail.outbox), original_amount + 1)
        self.assertEquals(temporary_data.area, self.arica)


class AreaFormTestCase(ProposingCycleTestCaseBase):
    def setUp(self):
        super(AreaFormTestCase, self).setUp()

    def test_area_form(self):
        data = {'area': self.arica.id}
        form = AreaForm(data)
        self.assertTrue(form.is_valid(), form.errors)
        cleaned_data = form.cleaned_data
        self.assertEquals(cleaned_data['area'], self.arica)

    @override_config(DEFAULT_AREA='whole_country')
    def test_area_form_default_value(self):
        whole_country = Area.objects.create(id=u'whole_country', name=u'A country')
        form = AreaForm()
        self.assertEquals(form.initial['area'], whole_country.id)

    @override_config(HIDDEN_AREAS='argentina')
    def test_area_form_is_staff_and_hidden_area(self):
        argentina = Area.objects.create(name=u'Argentina')
        data = {'area': argentina.id}
        form = AreaForm(data, is_staff=True)
        self.assertTrue(form.is_valid(), form.errors)
        cleaned_data = form.cleaned_data
        self.assertEquals(cleaned_data['area'], argentina)

class UpdateProposalWithAreaFormTestCase(ProposingCycleTestCaseBase):
    def setUp(self):
        super(UpdateProposalWithAreaFormTestCase, self).setUp()
        self.image = self.get_image()
        self.popular_proposal = PopularProposal.objects.create(proposer=self.fiera,
                                                               area=self.arica,
                                                               data=self.data,
                                                               title=u'This is a title'
                                                               )
        self.feli = User.objects.get(username='feli')
        self.feli.set_password('secr3t')
        self.feli.save()
        self.fiera.set_password('feroz')
        self.fiera.save()

    @override_settings(POSSIBLE_GENERATING_AREAS_FILTER='Comuna')
    def test_form_with_generated_at_form_valid(self):
        comuna = Area.objects.filter(classification='Comuna').first()
        update_data = {'background': u'Esto es un antecedente',
                       'contact_details': u'Me puedes contactar en el teléfono 123456',
                       'generated_at': comuna.id,
                       }
        file_data = {'image': self.image,
                     'document': self.get_document()}
        form = UpdateProposalForm(data=update_data,
                                  files=file_data,
                                  instance=self.popular_proposal)
        self.assertTrue(form.is_valid())
        proposal = form.save()
        self.assertEquals(proposal.generated_at, comuna)
        not_a_comuna = Area.objects.create(name='Not a Comuna')
        update_data['generated_at'] = not_a_comuna.id
        form = UpdateProposalForm(data=update_data,
                                  files=file_data,
                                  instance=self.popular_proposal)
        self.assertFalse(form.is_valid())

    @override_settings(POSSIBLE_GENERATING_AREAS_FILTER='Comuna')
    def test_form_with_generated_at_form_invalid(self):
        not_a_comuna = Area.objects.create(name='Not a Comuna')
        update_data = {'background': u'Esto es un antecedente',
                       'contact_details': u'Me puedes contactar en el teléfono 123456',
                       'generated_at': not_a_comuna,
                       }
        file_data = {'image': self.image,
                     'document': self.get_document()}
        form = UpdateProposalForm(data=update_data,
                                  files=file_data,
                                  instance=self.popular_proposal)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors['generated_at'])

    def test_get_update_view(self):
        url = reverse('popular_proposals:citizen_update', kwargs={'slug': self.popular_proposal.slug})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        self.client.login(username=self.feli.username, password='secr3t')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
        self.client.login(username=self.fiera.username, password='feroz')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['popular_proposal'], self.popular_proposal)
        self.assertTemplateUsed(response, 'popular_proposal/update.html')
        self.assertIsInstance(response.context['form'], UpdateProposalForm)