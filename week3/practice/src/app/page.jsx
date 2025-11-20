'use client';

import { useState } from "react";
import Header from "./_utils/Header";
import Sidebar from "./_utils/Sidebar";
import Dashboard from "./_utils/Dashboard";
import Layouts from "./_utils/Layouts";
import Pages from "./_utils/Pages";
import Charts from "./_utils/Charts";
import Tables from "./_utils/Tables";

export default function Home() {

  const [mainSection, setMainSection] = useState("dashboard");
  const [pageNumber, setPageNumber] = useState(1);
  const [layoutNum, setLayoutNum] = useState(1);

  const handleSidebarClick = (section) => {
    setMainSection(section);
  };

  const handlePageClick = (page)=>{
    setPageNumber(page)
    handleSidebarClick("pages")
  }

  const handleLayoutClick = (layoutNum)=>{
    setLayoutNum(layoutNum);
    handleSidebarClick("layouts");
  }

  const sections = {
    dashboard: <Dashboard />,
    layouts: <Layouts layoutNum = {layoutNum}/>,
    pages: <Pages pageNum={pageNumber} />,
    charts: <Charts />,
    tables: <Tables />
  };

  return (
    <main className="flex flex-col h-screen">
      <Header />

      <div className="flex flex-1">
        <Sidebar handleSidebarClick={handleSidebarClick} setPageNumber={handlePageClick} handleLayoutClick={handleLayoutClick}/>

        <section className="flex-1">
          {sections[mainSection]}
        </section>
      </div>
    </main>
  );
}
