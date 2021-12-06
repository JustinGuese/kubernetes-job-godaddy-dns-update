Docker / Kubernetes tool to update the IP on godaddy if the router changes IP adresses.

"Open Source" variant for DyDNS, no-ip and others.

Runs a kubernetes job every hour and updates the ip using a kubernetes cronjob

## environment variables

for docker just copy paste the `.env-example` and rename it to `.env`

for kubernetes create a secret with:

`kubectl create secret generic godaddy --from-literal=GODADDY_PUBLIC_KEY=2312123123 --from-literal=GODADDY_SECRET=123213123`