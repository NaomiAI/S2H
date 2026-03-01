# store2hydro

A modular two-stage **investment--dispatch framework** for evaluating
hydro storage retrofitting and spatial aggregation effects in
PyPSA-based energy system models.

------------------------------------------------------------------------

## Overview

`store2hydro` implements a structured pipeline that separates:

1.  **Planning (Investment Optimization)**
2.  **Dispatch (Operational Validation)**

The framework allows investment decisions derived on an aggregated or
simplified network to be validated on a higher-resolution operational
model.

This enables:

-   Studying spatial aggregation bias
-   Testing transfer mechanisms between model resolutions
-   Validating hydro storage retrofitting strategies
-   Building reproducible multi-stage workflows in PyPSA

------------------------------------------------------------------------

## Conceptual Architecture

Planning Network (n buses, coarse time resolution) ↓ solve
InvestSolution (capacities by zone / carrier) ↓ transfer Dispatch
Network (m buses, finer time resolution) ↓ solve Operational performance
metrics

The key design feature is an explicit **contract object**
(`InvestSolution`) that decouples planning and dispatch logic.

------------------------------------------------------------------------

## Repository Structure

store2hydro/ planning/ \# Investment model logic dispatch/ \# Dispatch
solver logic transfer/ \# Mapping investment → dispatch io/ \# Network
loading/saving utilities networks/ \# Network construction helpers

configs/ pipeline_demo.yaml

scripts/ run_pipeline_demo.py

tests/ test_pipeline_demo.py

------------------------------------------------------------------------

## Design Principles

-   Strict separation of planning and dispatch stages
-   Explicit investment contract (`InvestSolution`)
-   Config-driven execution (YAML-based)
-   PyPSA-native modeling (no custom solver wrappers)
-   Fully reproducible pipeline outputs
-   Minimal side effects between stages

------------------------------------------------------------------------

## Quickstart

Install in editable mode:

    pip install -e .

Run the demo pipeline:

    python scripts/run_pipeline_demo.py

Results are written to:

results/pipeline_demo/ investment/ investment_solved.nc
invest_solution.json dispatch/ dispatch_solved.nc report.txt

------------------------------------------------------------------------

## Stage 1 --- Planning

The planning stage:

-   Optionally subsets time
-   Adds hydro pumping retrofit candidates
-   Solves an investment problem
-   Extracts zonal retrofit capacities

Outputs:

-   Solved investment network (.nc)
-   InvestSolution JSON contract
-   Zonal investment summary

------------------------------------------------------------------------

## Stage 2 --- Dispatch

The dispatch stage:

-   Loads a higher-resolution network
-   Applies fixed capacities from InvestSolution
-   Solves operational dispatch
-   Produces validation metrics

Possible extensions:

-   Rolling horizon dispatch
-   Multi-year validation
-   Extreme weather stress testing
-   Curtailment and congestion analysis

------------------------------------------------------------------------

## Scientific Motivation

Large-scale energy system studies often rely on spatial aggregation
during investment optimization.

However, aggregation can distort:

-   Storage sizing
-   Curtailment behavior
-   Congestion patterns
-   Market values

This framework enables systematic testing of:

-   How investment decisions transfer across resolutions
-   Whether hydro retrofitting is robust to spatial detail
-   How aggregation biases scale with network complexity

------------------------------------------------------------------------

## Configuration

Execution is controlled via:

configs/pipeline_demo.yaml

Key sections:

-   investment
-   dispatch
-   transfer
-   solver
-   outputs

------------------------------------------------------------------------

## Roadmap

-   [x] Investment stage (StorageUnit retrofit)
-   [x] Dispatch validation stage
-   [x] Explicit investment contract
-   [ ] Rolling horizon dispatch
-   [ ] Generic transfer engine (YAML-driven)
-   [ ] Aggregation bias metrics module
-   [ ] Paper-ready experiment scripts
-   [ ] CI integration

------------------------------------------------------------------------

## Testing

Run:

    pytest -q

------------------------------------------------------------------------

## License

MIT 

------------------------------------------------------------------------

