#!/bin/bash
cd "$(dirname "$0")/phase1"
./apply-cellprotocol.sh --go
./apply-phase2.sh --go
