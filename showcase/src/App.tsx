import React from 'react';
import { Navbar } from './components/Navbar';
import { Hero } from './components/Hero';
import { PackageMeta } from './components/PackageMeta';
import { ProblemSolution } from './components/ProblemSolution';
import { CliShowcase } from './components/CliShowcase';
import { FeaturesGrid } from './components/FeaturesGrid';
import { ArchitectureDiagram } from './components/ArchitectureDiagram';
import { TechStack } from './components/TechStack';
import { EngineeringPractices } from './components/EngineeringPractices';
import { InstallationGuide } from './components/InstallationGuide';
import { Footer } from './components/Footer';

export const App: React.FC = () => {
  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Navbar />
      <main style={{ flex: 1 }}>
        <Hero />
        <PackageMeta />
        <ProblemSolution />
        <CliShowcase />
        <FeaturesGrid />
        <ArchitectureDiagram />
        <TechStack />
        <EngineeringPractices />
        <InstallationGuide />
      </main>
      <Footer />
    </div>
  );
};

export default App;
