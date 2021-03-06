from django.contrib import admin
from django import forms
from django.forms.utils import ErrorList
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from nadine.models import *

# Register the objects with the admin interface
admin.site.register(Neighborhood)
admin.site.register(Industry)
admin.site.register(HowHeard)
admin.site.register(MembershipPlan)
admin.site.register(Room)
admin.site.register(Event)


class StyledAdmin(admin.ModelAdmin):

    class Media:
        css = {"all": ('local-admin.css', )}


class TransactionAdmin(StyledAdmin):
    list_display = ('transaction_date', 'user', 'amount')
    search_fields = ('user__first_name', 'user__last_name', 'amount')
    raw_id_fields = ('bills', 'user')
admin.site.register(Transaction, TransactionAdmin)


class BillAdmin(StyledAdmin):
    list_display = ('bill_date', 'user', 'amount')
    search_fields = ('user__first_name', 'user__last_name')
    raw_id_fields = ('membership', 'dropins', 'guest_dropins')
admin.site.register(Bill, BillAdmin)


class BillingLogAdmin(StyledAdmin):
    list_display = ('started', 'ended', 'note', 'successful')
admin.site.register(BillingLog, BillingLogAdmin)


# class EmergencyContactAdmin(StyledAdmin):
#     list_display = ('user', 'name', 'relationship', 'phone', 'email', 'last_updated')
#     search_fields = ('user__username', 'user__first_name', 'user__last_name')
# admin.site.register(EmergencyContact, EmergencyContactAdmin)
# class XeroContactAdmin(StyledAdmin):
#     list_display = ('user', 'xero_id', 'last_sync')
#     search_fields = ('user__username', 'user__first_name', 'user__last_name')
# admin.site.register(XeroContact, XeroContactAdmin)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    max_num = 1
class EmailAddressInline(admin.TabularInline):
    model = EmailAddress
    fields=['id', 'is_primary', 'email', 'verified_ts',]
    readonly_fields=['id', 'is_primary', 'verified_ts', ]
    extra = 0
class EmergencyContactInline(admin.StackedInline):
    model = EmergencyContact
    can_delete = False
    max_num = 1
class XeroContactInline(admin.TabularInline):
    model = XeroContact
    readonly_fields=['last_sync', ]
    can_delete = False
    max_num = 1
class UserWithProfileAdmin(UserAdmin):
    inlines = [EmailAddressInline, UserProfileInline, EmergencyContactInline, XeroContactInline]
admin.site.unregister(User)
admin.site.register(User, UserWithProfileAdmin)

class CoworkingDayAdmin(StyledAdmin):
    list_display = ('visit_date', 'user', 'paid_by', 'created_ts')
    search_fields = ('user__first_name', 'user__last_name', 'paid_by__first_name', 'paid_by__last_name')
admin.site.register(CoworkingDay, CoworkingDayAdmin)


class MembershipAdmin(StyledAdmin):
    list_display = ('user', 'start_date', 'end_date')
    search_fields = ('user__first_name', 'user__last_name')
admin.site.register(Membership, MembershipAdmin)


class SentEmailLogAdmin(StyledAdmin):
    list_display = ('created', 'recipient', 'subject', 'note', 'success')
admin.site.register(SentEmailLog, SentEmailLogAdmin)


class SecurityDepositAdmin(StyledAdmin):
    list_display = ('user', 'received_date', 'returned_date', 'amount', 'note')
admin.site.register(SecurityDeposit, SecurityDepositAdmin)


class SpecialDayAdmin(StyledAdmin):
    list_display = ('user', 'year', 'month', 'day', 'description')
admin.site.register(SpecialDay, SpecialDayAdmin)


class MemberNoteAdmin(StyledAdmin):
    list_display = ('created', 'user', 'created_by', 'note')
admin.site.register(MemberNote, MemberNoteAdmin)


class MemberAlertAdmin(StyledAdmin):
    def unresolve(self, request, queryset):
        for alert in queryset:
            alert.resolved_ts = None
            alert.resolved_by = None
            alert.muted_ts = None
            alert.muted_by = None
            alert.save()
        self.message_user(request, "Alerts Unresolved")

    list_display = ('created_ts', 'key', 'user', 'resolved_ts', 'resolved_by', 'muted_ts', 'muted_by', 'note')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    list_filter = ('key', )
    actions = ["unresolve", ]
admin.site.register(MemberAlert, MemberAlertAdmin)


class FileUploadAdmin(StyledAdmin):
    list_display = ('uploadTS', 'user', 'name')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    list_filter = ('document_type',)
admin.site.register(FileUpload, FileUploadAdmin)




# Copyright 2016 Office Nomads LLC (http://www.officenomads.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
