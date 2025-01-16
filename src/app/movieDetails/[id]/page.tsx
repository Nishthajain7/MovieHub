'use client';
import { useRouter } from "next/router";
import { useParams } from "next/navigation";
import movies from "../../../../public/movies.json";
import Image from 'next/image';

const MovieDetails = () => {
    const { id } = useParams(); // Get the movie ID from the URL

    // Find the movie based on the ID
    const movie = movies.find((movie) => movie.id === parseInt(id as string, 10));

    if (!movie) return <div>Movie not found!</div>;

    return (
        // <div>
        //     <Image src={movie.image} width={500} height={500} alt={movie.name} className="object-fill" />
        //     <h1>{movie.name}</h1>
        //     <p>Release Year: {movie.year}</p>
        //     <p>{movie.description}</p>
        // </div>

        <div className="flex sm:flex-col md:flex-row lg:flex-row gap-6 p-6">
            <img src={movie.image} alt={movie.name} className="object-cover" />
            <div>
                <h1 className="text-4xl font-semibold pb-5">{movie.name}</h1>
                <p className="text-lg text-gray-700 pb-4"><strong>Release Year:</strong> {movie.year}</p>
                <p className="text-gray-600">{movie.description}</p>
            </div>
        </div>
    );
};

export default MovieDetails;
