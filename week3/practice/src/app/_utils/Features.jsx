import React from 'react'

const Features = () => {
    return (
        <section className="py-20 px-6 sm:px-12">
            <h2 className="text-3xl font-semibold text-center mb-12">Features</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
                <div className="feature-card bg-white p-6 rounded-lg shadow-lg text-center">
                    <h3 className="text-xl font-semibold mb-4">Feature 1</h3>
                    <p className="text-gray-600">
                        Some powerful description of the feature goes here. It's easy to use.
                    </p>
                </div>
                <div className="feature-card bg-white p-6 rounded-lg shadow-lg text-center">
                    <h3 className="text-xl font-semibold mb-4">Feature 2</h3>
                    <p className="text-gray-600">
                        Describe another great feature of the product that stands out.
                    </p>
                </div>
                <div className="feature-card bg-white p-6 rounded-lg shadow-lg text-center">
                    <h3 className="text-xl font-semibold mb-4">Feature 3</h3>
                    <p className="text-gray-600">
                        This feature helps you increase productivity and efficiency.
                    </p>
                </div>
            </div>
        </section>
    )
}

export default Features