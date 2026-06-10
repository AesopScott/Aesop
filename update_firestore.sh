#!/bin/bash

# Firebase credentials
PROJECT_ID="playagame-f733d"
CLIENT_EMAIL="firebase-adminsdk-fbsvc@playagame-f733d.iam.gserviceaccount.com"
PRIVATE_KEY="-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCsD6hEwl5592/q
N0SSBpQ77oYeww7H7qNOorn15Y5vxPiHnZLSCRtF/YVjmz7bhFZHUOyi+jpr4+T3
uazVfFPqBgoOcbigYh8PIiRfIfnbk+u9270piVNr7hLpc3/MrB6copPVea05/QRb
biOINxtaFZS6bR32/CIzBHaO7Bf6uJEN/zsb4jCPtsEoMzSSkIS5KmcPrDgaxg5U
8PZa245LJOyLVcrpDNFc1vr/09xoWHzMjmDocESdB7d1kvcYx61Z2mIyNz9/ihpi
UGeVS/wS+nLyzZac3648CeTjSEKGkdoTKVX53fhLx9oSiLVt4a5vVr6/dP9Gfhcs
twiRxlINAgMBAAECggEAA7i0+YPAul+dNpIqdAQbaa5vjTPH2pAxTQ6c+hIUghtf
CsPgPJXA1sM0guKFOgdDPHimHaJO6C1+MtN7xwRQ5lNqHUTdau6kYFXrNnmMJ3Es
HKenkEHtoXx9QTpjzb/9S4MCso/WrNXppbacoyIZ/9lOpbedec2bScIzdETsAdq6
BlnnCAQs3+1CkH1RmIF1kmfmK4Ko0sRRPnf8NI2V5TB6z1rC9crEDAJEg9x2ClYc
uU5PXp7wr7SiwFvwyQ8+LZ902coLh+xj1idPiYzRrPGR49Gv7GsyV+6fwMoB/k5k
IlUhncax7xpWzNSlxbJ3cJ5q5frHdzUphCTbe7mKqwKBgQDaiSaaetrC+GcOySnC
V2jAFEmmXKHGBChj/9qhoRPSK28XP4i8i/BlGIZutiT4HwAYkHKtMMatxU0fclde
d0C0Yfe93eHhgYz5sbgXP6MHZJ1m+NQlDxf+kPlDCq1Y8y0TpcVEqrCyjeIGFbrg
3kSBJK8CTFgeiij/vyvS0p02owKBgQDJjuHzFmGoRHtnSXnxxCFXxE65ZsSsho/w
FR0ScFBeKZNWucX0tXlHvHJn9srP6lKC3Hl96UV7RmDX8iGncKuAQv2OV5pjgZHl
FYYJ7QdHQgy1wptOrdCUGoA1l6Hnn2ykWAg97yHEMrJIzgnFVBAxs23Csuw3VejI
FuD4x43PjwKBgBN5RUdeyz+0gvp+UopO37a+GBILDx9mH3NJyWG9yNZhqHSZ5MVo
cvOPS+txr7msiYWm2ZE1V38Epeq3dbGlTs7ELB9vNkGyGa3meFEaCp0OCjiy07S5
s5mrsYqX2PqkMNAfZYTI8RX4Lrv8E7sWE2SusCm0Q+X0ydKAZpdSzU+hAoGAJeCw
HZqrJ5AXEMYCIKkXCwNdOAJUG4f+LMQK/pgUwl1VzwqCZQZlkFGdvmPmoUQL1YPR
YRQhdpU3Rd2+7VSDJktwkvtrjB+hZ0ewNNVSdNW4xb+YqCSJ+gsw5OFmD70qEYhp
pBn4YoKUdpIhy++MS4rIqbouIggHAvMpvBbkU4kCgYBGmBl4YuRWtTvJNk77bUqg
I/aTL0tuPM24SiVGUWN9hFPcbEUmYYyKS2HhQshHjBEXaA/6biEll0G4B5FcwO7s
nyjBi6S2ADiFTC9dW3P1nnG5v8wkEi22F7UK26/JDWSCdZgxD+IxyUt5+msbQCrs
otxxHorJUCIafQ1NfUfBfg==
-----END PRIVATE KEY-----"

LEARNER_ID="AESOP-YAPT"
EARNED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Create JWT token
cat > jwt_payload.json << PAYLOAD
{
  "iss": "$CLIENT_EMAIL",
  "scope": "https://www.googleapis.com/auth/datastore",
  "aud": "https://oauth2.googleapis.com/token",
  "exp": $(($(date +%s) + 3600)),
  "iat": $(date +%s)
}
PAYLOAD

# For now, let's use a simpler approach - write directly via Node script with better error handling
echo "Using Node.js to update Firestore..."
