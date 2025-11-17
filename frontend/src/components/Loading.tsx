// import Loader from "../assets/loader.gif"
import { Player } from "@lottiefiles/react-lottie-player"
import LoaderJson from '../assets/loaderj.json'

export default function Loading() {
    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-30 backdrop-blur-sm">
            {/* <div className="text-white text-xl font-semibold animate-pulse">
                <img src={Loader} className="w-52 h-52 animate-bounce duration-300" alt="Loading..." />
            </div> */}
            <Player
                autoplay
                loop
                src={LoaderJson}
                className="w-52 h-52 animate-bounce duration-150"
            />
        </div>
    );
}
