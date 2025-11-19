'use client';

import { useState } from "react";
import Header from "./_components/Header";
import Sidebar from "./_components/Sidebar";
import Dashboard from "./_components/Dashboard";
import Layouts from "./_components/Layouts";
import Pages from "./_components/Pages";
import Charts from "./_components/Charts";
import Tables from "./_components/Tables";

export default function Home() {

  const [mainSection, setMainSection] = useState("dashboard");

  const handleSidebarClick = (section) => {
    setMainSection(section);
  };

  const sections = {
    dashboard: <Dashboard />,
    layouts: <Layouts />,
    pages: <Pages />,
    charts: <Charts />,
    tables: <Tables />
  };

  return (
    <main className="flex flex-col h-screen">
      <Header />

      <div className="flex flex-1">
        <Sidebar handleSidebarClick={handleSidebarClick} />

        <section className="flex flex-1 p-4 items-center justify-center">
          {sections[mainSection]}
        </section>
      </div>
    </main>
  );
}
