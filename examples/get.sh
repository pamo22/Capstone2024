
declare -a arr=("https://www.adobe.com/au/legal/licenses-terms.html" "https://www.adobe.com/au/legal/terms.html" "https://www.adobe.com/content/dam/cc/en/legal/licenses-terms/pdf/CS6.pdf" "https://www.adobe.com/content/dam/cc/en/legal/licenses-terms/pdf/CC_EULA Gen WWCombined-MULTI-20121017_1230.pdf" "https://www.adobe.com/content/dam/cc/en/legal/licenses-terms/pdf/Captivate 2019.pdf" "https://www.servicenow.com/content/dam/servicenow-assets/public/en-us/doc-type/legal/servicenow-general-terms-and-conditions-02-11-2020.pdf" "https://docs.broadcom.com/doc/end-user-agreement-english" "https://www.redhat.com/licenses/Enterprise-Agreement-Webversion-APAC-Australia-English-202111.pdf" "https://www.redhat.com/licenses/Red Hat GPLv2-Based EULA 20191118.pdf" "https://www.redhat.com/licenses/Appendix_1_Global English 20231205.pdf" "https://www.redhat.com/en/about/agreements" "https://www.salesforce.com/company/legal/customer-agreements/" "https://www.salesforce.com/content/dam/web/en_us/www/documents/legal/salesforce_MSA.pdf" "https://www.microfocus.com/en-us/legal/software-licensing" "https://www.microfocus.com/media/documentation/micro_focus_end user_license_agreement.pdf" "https://www.microfocus.com/media/documentation/additional-license-authorizations-for-legacy-cobol-and-enterprise-software-products-documentation.pdf" "https://www.oracle.com/downloads/licenses/no-fee-license.html" "https://www.microsoft.com/licensing/terms/welcome/WelcomePage?programMoniker=all" "https://www.ibm.com/support/customer/csol/terms")



for n in "${arr[@]}"
do
	wget "$n" --tries=1
done
