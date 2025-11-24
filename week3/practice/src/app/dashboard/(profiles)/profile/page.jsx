"use client";

import React from "react";
import { FaArrowLeft } from "react-icons/fa";
import { useRouter } from "next/navigation";
import Image from "next/image";

const ProfilePage = () => {
  const router = useRouter();

  return (
    <main className="p-4 md:p-8 lg:p-12">

      <nav aria-label="Go back">
        <a
          className="cursor-pointer flex items-center gap-2 text-blue-600 underline mb-6"
          onClick={() => router.back()}
        >
          <FaArrowLeft /> Go back
        </a>
      </nav>

      <section className="border rounded-lg p-4 md:p-6 grid grid-cols-1 md:grid-cols-3 gap-6 bg-white">

        <figure className="flex justify-center md:justify-start">
          <Image
            src="https://media.istockphoto.com/id/1317804578/photo/one-businesswoman-headshot-smiling-at-the-camera.jpg?s=612x612&w=0&k=20&c=EqR2Lffp4tkIYzpqYh8aYIPRr-gmZliRHRxcQC5yylY="
            alt="Profile picture"
            width={400}
            height={400}
            className="rounded-lg object-cover w-full h-auto"
          />
          <figcaption className="sr-only">Profile picture</figcaption>
        </figure>

        <article className="md:col-span-2 grid grid-cols-1 md:grid-cols-2 gap-8">

          <section className="space-y-6">
            <div>
              <h2 className="text-sm text-gray-500">Name</h2>
              <p className="text-lg font-semibold">Nina Valentine</p>
            </div>

            <div>
              <h2 className="text-sm text-gray-500">Job Title</h2>
              <p className="text-gray-700">Actress</p>
            </div>

            <div>
              <h2 className="text-sm text-gray-500">Email</h2>
              <a
                href="mailto:nina_val@example.com"
                className="text-blue-600 hover:underline"
              >
                nina_val@example.com
              </a>
            </div>
          </section>

          <section className="space-y-6">
            <div>
              <h2 className="text-sm text-gray-500">LinkedIn</h2>
              <a
                href="https://linkedin.com"
                className="text-blue-600 hover:underline"
              >
                linkedin.com
              </a>
            </div>

            <div>
              <h2 className="text-sm text-gray-500">Twitter</h2>
              <a
                href="https://x.com"
                className="text-blue-600 hover:underline"
              >
                www.x.com
              </a>
            </div>

            <div>
              <h2 className="text-sm text-gray-500">Facebook</h2>
              <a
                href="https://facebook.com"
                className="text-blue-600 hover:underline"
              >
                facebook.com
              </a>
            </div>
          </section>

        </article>
      </section>

      <section className="mt-6 p-4">
        <h2 className="text-gray-700 font-semibold mb-2">Bio</h2>
        <article className="text-gray-600 leading-relaxed">
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent
          aliquet odio augue, in dapibus lacus imperdiet ut. Quisque elementum
          placerat neque rhoncus tempus. Cras id suscipit diam, sit amet rutrum
          ipsum. Vestibulum rutrum elit lacinia sapien porta pulvinar. Neque
          rhoncus tempus. Cras id suscipit diam, sit amet rutrum ipsum.
        </article>

        <nav className="mt-4">
          <a href="#" className="text-blue-600 hover:underline font-medium">
            Edit Profile
          </a>
        </nav>
      </section>

    </main>
  );
};

export default ProfilePage;
