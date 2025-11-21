'use client'
import React, { useState } from 'react'
import Card from '@/components/ui/Card'
import Modal from '@/components/ui/Modal';
import AreaChart from '../_utils/AreaChart';
import BarChart from '../_utils/BarChart';
import ChartCard from '@/components/ui/ChartCard';
import { IoBarChart } from "react-icons/io5";
import { AiOutlineAreaChart } from "react-icons/ai";
import { FaTable } from "react-icons/fa";
import Table from '../_utils/Table';




const Dashboard = () => {
  const cards = [
    {
      label: "Primary Card",
      color: "blue",
      details: "This is the primary card details."
    },
    {
      label: "Winning Card",
      color: "#b45309",
      details: "This card shows the winning stats."
    },
    {
      label: "Success Card",
      color: "#16a34a",
      details: "This card represents a successful state. Lorem ipsum dolor sit amet consectetur adipisicing elit. Tenetur, impedit officiis? Eum reprehenderit impedit suscipit qui ea quas minus delectus ullam sequi, labore officia ut maxime doloremque, rem praesentium nihil.Lorem ipsum dolor sit amet consectetur adipisicing elit. Tenetur, impedit officiis? Eum reprehenderit impedit suscipit qui ea quas minus delectus ullam sequi, labore officia ut maxime doloremque, rem praesentium nihil.Lorem ipsum dolor sit amet consectetur adipisicing elit. Tenetur, impedit officiis? Eum reprehenderit impedit suscipit qui ea quas minus delectus ullam sequi, labore officia ut maxime doloremque, rem praesentium nihil.Lorem ipsum dolor sit amet consectetur adipisicing elit. Tenetur, impedit officiis? Eum reprehenderit impedit suscipit qui ea quas minus delectus ullam sequi, labore officia ut maxime doloremque, rem praesentium nihil."
    },
    {
      label: "Danger Card",
      color: "#dc2626",
      details: "This card indicates a danger state."
    },
  ];
  const [showModal, setShowModal] = useState(false);
  const [modalDetials, setModalDetails] = useState("");

  const handleModalClose = () => {
    setShowModal(false);
    setModalDetails("");
  }
  const handleModalOpen = (details) => {
    setModalDetails(details);
    setShowModal(true);
  }
  return (
    <section className='px-7 py-8'>
      <h1 className='font-bold text-5xl'>Dashboard</h1>
      <p className='w-full bg-[#f0f0f0] px-5 py-2 font-semibold text-lg my-3 rounded-md text-gray-500'>DashBoard</p>
      <section className='flex justify-center flex-wrap gap-2 items-start xs:justify-center sm:justify-center md:justify-between'>
        {
          cards.map((card, index) => (
            <Card key={index} label={card.label} color={card.color} details={card.details} handleModalOpen={handleModalOpen} />
          ))
        }{
          showModal && <Modal handleModalClose={handleModalClose} modalDetails={modalDetials} />
        }
      </section>
      <section className='grid grid-cols-1 md:grid-cols-2 gap-2 mt-3'>
        <div className=''>
          <ChartCard title={"Area Chart Example"} logo={<AiOutlineAreaChart />}>
            <AreaChart />
          </ChartCard>
        </div>
        <div className=''>
          <ChartCard title={"Bar Chart Example"} logo={<IoBarChart />}>
            <BarChart />
          </ChartCard>
        </div>
      </section>
      <section className=" p-4">
        <h2 className="text-2xl font-semibold mb-4 flex gap-4"> <FaTable/> Data Table Example</h2>
        <Table />
      </section>
    </section>
  )
}

export default Dashboard