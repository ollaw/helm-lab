set -e
kubectx main-qa
TEAM=team1 envsubst < namespaces.yaml | kubectl apply -f -
TEAM=team2 envsubst < namespaces.yaml | kubectl apply -f -
TEAM=team3 envsubst < namespaces.yaml | kubectl apply -f -
TEAM=team4 envsubst < namespaces.yaml | kubectl apply -f -
