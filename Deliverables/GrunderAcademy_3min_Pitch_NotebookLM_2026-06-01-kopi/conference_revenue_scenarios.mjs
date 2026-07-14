#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";

const NOK = "NOK";

const policy = {
  id: "policy:dimy.conference.scenario.v0.2026-05-14",
  pspRate: 0.025,
  pspFixedNOK: 1,
  riskBufferRate: 0.05,
  allocation: {
    operator: 0.55,
    commons: 0.2,
    participantBenefit: 0.25
  },
  regulatoryBoundary: {
    productVariant: "access entitlement + usage quota + single-domain benefit simulation",
    transferable: false,
    cashOut: false,
    externalAcceptance: false
  }
};

const unitCosts = {
  storagePerParticipantNOK: 3,
  storagePerSponsorNOK: 20,
  runtimePerParticipantNOK: 8,
  runtimePerSponsorNOK: 50,
  mediaPerParticipantHour: {
    small: 1.2,
    medium: 1.1,
    large: 1,
    expo: 0.9
  },
  aiProviderPerAIUserNOK: {
    small: 3,
    medium: 4,
    large: 5,
    expo: 5
  },
  leadVaultCostPerUnlockNOK: {
    small: 25,
    medium: 22,
    large: 20,
    expo: 18
  },
  leadVaultOpsPerSponsorNOK: 150,
  supportPerSponsorNOK: 1000,
  auditCostPerUnlockNOK: 8,
  auditFixedNOK: {
    small: 3000,
    medium: 8500,
    large: 25000,
    expo: 60000
  }
};

const scenarios = [
  {
    id: "small-120",
    label: "Lite fagarrangement",
    sizeBand: "small",
    participants: 120,
    sponsors: 4,
    days: 1,
    liveHours: 5,
    leadUnlocks: 40,
    aiAttachRate: 0.35,
    pricing: {
      organizerPackageNOK: 25000,
      participantPlatformFeeNOK: 85,
      sponsorPackageNOK: 8000,
      leadUnlockPriceNOK: 750,
      aiConciergeFeePerAIUserNOK: 40,
      auditTransparencyPackageNOK: 7500
    },
    fixedSupportNOK: 12000
  },
  {
    id: "medium-500",
    label: "Mellomstor bransjekonferanse",
    sizeBand: "medium",
    participants: 500,
    sponsors: 15,
    days: 2,
    liveHours: 16,
    leadUnlocks: 450,
    aiAttachRate: 0.45,
    pricing: {
      organizerPackageNOK: 85000,
      participantPlatformFeeNOK: 75,
      sponsorPackageNOK: 12000,
      leadUnlockPriceNOK: 700,
      aiConciergeFeePerAIUserNOK: 55,
      auditTransparencyPackageNOK: 25000
    },
    fixedSupportNOK: 40000
  },
  {
    id: "large-1500",
    label: "Stor industrikonferanse",
    sizeBand: "large",
    participants: 1500,
    sponsors: 45,
    days: 3,
    liveHours: 30,
    leadUnlocks: 2200,
    aiAttachRate: 0.55,
    pricing: {
      organizerPackageNOK: 250000,
      participantPlatformFeeNOK: 65,
      sponsorPackageNOK: 18000,
      leadUnlockPriceNOK: 650,
      aiConciergeFeePerAIUserNOK: 65,
      auditTransparencyPackageNOK: 80000
    },
    fixedSupportNOK: 110000
  },
  {
    id: "expo-5000",
    label: "Expo / stort hybridt event",
    sizeBand: "expo",
    participants: 5000,
    sponsors: 120,
    days: 4,
    liveHours: 50,
    leadUnlocks: 9000,
    aiAttachRate: 0.5,
    pricing: {
      organizerPackageNOK: 700000,
      participantPlatformFeeNOK: 50,
      sponsorPackageNOK: 25000,
      leadUnlockPriceNOK: 550,
      aiConciergeFeePerAIUserNOK: 60,
      auditTransparencyPackageNOK: 220000
    },
    fixedSupportNOK: 300000
  }
];

function round(value) {
  return Math.round(value);
}

function pct(value) {
  return Math.round(value * 1000) / 10;
}

function money(value) {
  return `${round(value).toLocaleString("nb-NO")} ${NOK}`;
}

function computeScenario(scenario) {
  const aiUsers = scenario.participants * scenario.aiAttachRate;
  const revenue = {
    organizerPackageNOK: scenario.pricing.organizerPackageNOK,
    participantPlatformNOK: scenario.participants * scenario.pricing.participantPlatformFeeNOK,
    sponsorPackagesNOK: scenario.sponsors * scenario.pricing.sponsorPackageNOK,
    leadUnlockNOK: scenario.leadUnlocks * scenario.pricing.leadUnlockPriceNOK,
    aiConciergeNOK: aiUsers * scenario.pricing.aiConciergeFeePerAIUserNOK,
    auditTransparencyNOK: scenario.pricing.auditTransparencyPackageNOK
  };
  const grossRevenueNOK = Object.values(revenue).reduce((sum, value) => sum + value, 0);

  const paymentTransactions = 1 + scenario.sponsors;
  const directCosts = {
    pspFeeNOK: grossRevenueNOK * policy.pspRate + paymentTransactions * policy.pspFixedNOK,
    storageNOK: scenario.participants * unitCosts.storagePerParticipantNOK + scenario.sponsors * unitCosts.storagePerSponsorNOK,
    runtimeNOK: scenario.participants * unitCosts.runtimePerParticipantNOK + scenario.sponsors * unitCosts.runtimePerSponsorNOK,
    mediaBandwidthNOK: scenario.participants * scenario.liveHours * unitCosts.mediaPerParticipantHour[scenario.sizeBand],
    aiProviderNOK: aiUsers * unitCosts.aiProviderPerAIUserNOK[scenario.sizeBand],
    leadVaultOpsNOK: scenario.leadUnlocks * unitCosts.leadVaultCostPerUnlockNOK[scenario.sizeBand] + scenario.sponsors * unitCosts.leadVaultOpsPerSponsorNOK,
    supportNOK: scenario.fixedSupportNOK + scenario.sponsors * unitCosts.supportPerSponsorNOK,
    auditExportNOK: unitCosts.auditFixedNOK[scenario.sizeBand] + scenario.leadUnlocks * unitCosts.auditCostPerUnlockNOK,
    riskBufferNOK: grossRevenueNOK * policy.riskBufferRate
  };
  const totalCostNOK = Object.values(directCosts).reduce((sum, value) => sum + value, 0);
  const grossMarginNOK = grossRevenueNOK - totalCostNOK;
  const positiveMarginNOK = Math.max(0, grossMarginNOK);
  const allocation = {
    dimyOperatorNOK: positiveMarginNOK * policy.allocation.operator,
    havenCommonsNOK: positiveMarginNOK * policy.allocation.commons,
    participantBenefitSimulationNOK: positiveMarginNOK * policy.allocation.participantBenefit
  };

  const cellRevenueAttribution = {
    "ConferencePublishedContentCell + ConferencePublicShellCell": revenue.organizerPackageNOK * 0.25,
    "ConferenceRegistrationCell + ConferenceOnboardingCell + ConferencePublicProfileCell": revenue.participantPlatformNOK,
    "ConferenceAgendaCell + ConferenceRecommendationCell + ConferenceSchedulingCell + ConferenceConnectionHubCell": revenue.organizerPackageNOK * 0.25,
    "ConferenceConciergeCell + AIGatewayCell": revenue.aiConciergeNOK,
    "ConferenceInsightAggregateCell + ConferenceOrganizerProjectionCell": revenue.organizerPackageNOK * 0.2 + revenue.auditTransparencyNOK * 0.35,
    "ConferenceSponsorLeadAggregateCell + LeadVaultCell + ConsentReceiptCell + ExhibitorAccessCell": revenue.sponsorPackagesNOK + revenue.leadUnlockNOK,
    "ValueFlowViewerCell + AuditExport": revenue.auditTransparencyNOK * 0.65,
    "JitsiConferenceGatekeeperCell / media adapter": revenue.organizerPackageNOK * 0.3
  };

  return {
    id: scenario.id,
    label: scenario.label,
    drivers: {
      participants: scenario.participants,
      sponsors: scenario.sponsors,
      days: scenario.days,
      liveHours: scenario.liveHours,
      leadUnlocks: scenario.leadUnlocks,
      aiUsers: round(aiUsers)
    },
    pricing: scenario.pricing,
    revenue,
    grossRevenueNOK,
    directCosts,
    totalCostNOK,
    grossMarginNOK,
    grossMarginPercent: grossRevenueNOK === 0 ? 0 : grossMarginNOK / grossRevenueNOK,
    allocation,
    dimyOperatorPercentOfGrossRevenue: grossRevenueNOK === 0 ? 0 : allocation.dimyOperatorNOK / grossRevenueNOK,
    leadVaultShareOfRevenue: grossRevenueNOK === 0 ? 0 : (revenue.sponsorPackagesNOK + revenue.leadUnlockNOK) / grossRevenueNOK,
    sensitivity: {
      plusMinus100NOKPerUnlockImpactNOK: scenario.leadUnlocks * 100,
      plusMinus10PercentSponsorPackageImpactNOK: revenue.sponsorPackagesNOK * 0.1,
      plusMinus1NOKPerParticipantHourMediaImpactNOK: scenario.participants * scenario.liveHours
    },
    cellRevenueAttribution
  };
}

function toCsv(rows) {
  const headers = [
    "id",
    "label",
    "participants",
    "sponsors",
    "leadUnlocks",
    "grossRevenueNOK",
    "totalCostNOK",
    "grossMarginNOK",
    "grossMarginPercent",
    "dimyOperatorNOK",
    "havenCommonsNOK",
    "participantBenefitSimulationNOK",
    "leadVaultShareOfRevenue"
  ];
  const lines = [headers.join(",")];
  for (const row of rows) {
    lines.push([
      row.id,
      JSON.stringify(row.label),
      row.drivers.participants,
      row.drivers.sponsors,
      row.drivers.leadUnlocks,
      round(row.grossRevenueNOK),
      round(row.totalCostNOK),
      round(row.grossMarginNOK),
      pct(row.grossMarginPercent),
      round(row.allocation.dimyOperatorNOK),
      round(row.allocation.havenCommonsNOK),
      round(row.allocation.participantBenefitSimulationNOK),
      pct(row.leadVaultShareOfRevenue)
    ].join(","));
  }
  return lines.join("\n") + "\n";
}

const results = scenarios.map(computeScenario);

for (const result of results) {
  console.log(`${result.id} | gross=${money(result.grossRevenueNOK)} | cost=${money(result.totalCostNOK)} | margin=${money(result.grossMarginNOK)} | DiMy operator=${money(result.allocation.dimyOperatorNOK)} | LeadVault share=${pct(result.leadVaultShareOfRevenue)}%`);
}

if (process.argv.includes("--write")) {
  const outDir = path.join("ValueRedistribution", "outputs");
  fs.mkdirSync(outDir, { recursive: true });
  fs.writeFileSync(
    path.join(outDir, "conference_revenue_scenarios_2026-05-14.json"),
    JSON.stringify({
      version: "conference-revenue-scenarios/v0",
      generatedAt: "2026-05-14",
      currency: NOK,
      policy,
      unitCosts,
      scenarios: results
    }, null, 2) + "\n"
  );
  fs.writeFileSync(
    path.join(outDir, "conference_revenue_scenarios_2026-05-14.csv"),
    toCsv(results)
  );
}

